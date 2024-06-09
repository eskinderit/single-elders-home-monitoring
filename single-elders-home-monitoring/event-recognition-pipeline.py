#################################################### PARAMS ####################################################
# parameter to simulate the pyspark pipeline with `n_copies` of the original dataframe, replication
N_COPIES = 5
LOG = True
TRAIN_PCA = False
LOCAL = True

if LOCAL:
    import os
    import sys
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    import findspark
    findspark.init()
    # default config for local
    TRAIN_PCA = True
    INPUT_CSV_URL = './data/database_gas.csv'
    NOISE_CSV_URL = './data/data_ref_until_2020-02-13.csv'
else:
    NOISE_PCA_URL = 'hdfs://spark-master:8020/user/root/vagrant/noisePCA'
    INPUT_CSV_URL ='hdfs://spark-master:8020/user/root/vagrant/database_gas.csv'
    NOISE_CSV_URL = 'hdfs://spark-master:8020/user/root/vagrant/data_ref_until_2020-02-13.csv'
#################################################### IMPORTING LIBRARIES ####################################################
 # local
import pandas as pd
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession 

spark = (SparkSession.
     builder. # master('local[*]'). leave out for cluster mode
     appName('single-elders-monitoring').
#     config(conf = SparkConf()).
     getOrCreate())

import matplotlib.pyplot as plt
import numpy as np
from pyspark.sql.functions import asc
from pyspark.sql.window import Window
from pyspark.sql import functions as F
from pyspark.ml.feature import VectorAssembler, StandardScaler, PCA, PCAModel
from pyspark.sql.functions import col, concat, dayofmonth, hour, month, year
from pyspark.sql.functions import lit
from pyspark.ml.functions import vector_to_array
from pyspark.sql.types import FloatType, IntegerType

###################################################### IMPORTING DATA #######################################################
if LOG:
    print('_'*20,'START: importing original dataset','_'*20)

occupants_df = spark.read.csv(INPUT_CSV_URL, header=True,inferSchema=True) \
                            .where("timestamp < '2020-01-25'")\
                            .withColumn("housing_unit",lit(0))

if LOG:
    occupants_df.show()
    print('_'*20,'END: importing original dataset','_'*20)
    print('Original dataset has {} rows and {} columns.'.format(occupants_df.count(), len(occupants_df.columns)))
    print('Original dataset has features:', occupants_df.columns)
    print('Original dataset is going to be replicated {} times (excluded itself).'.format(N_COPIES))
    print('_'*20,'START: replicating original dataset','_'*20)

# adding original dataframe copies as if they were other housing units
df_copies = []
for i in range(N_COPIES):
    df_copies.append(occupants_df.select("*").withColumn("housing_unit", lit(i+1)))
for i in df_copies:
    occupants_df = occupants_df.union(i)

if LOG:
    print('_'*20, 'END: replicating original dataset','_'*20)
    print('Replicated dataset has {} rows and {} columns.'.format(occupants_df.count(), len(occupants_df.columns)))

################################################ MEDIAN FILTER APPLICATION ##################################################
# applied separately for each using unit
window_size=11
windowSpec = Window.partitionBy("housing_unit").orderBy(asc("timestamp")).rowsBetween(-window_size//2, window_size//2) # daily partitioning
rolling_median_udf = F.udf(lambda x: float(np.median(x)), FloatType())
cols_to_process = occupants_df.columns.copy()
cols_to_process.remove('timestamp')
cols_to_process.remove('housing_unit')
conversion_dict = {column: rolling_median_udf(F.collect_list(column).over(windowSpec)) for column in cols_to_process}
if LOG:
    print('_'*20, 'START: Median filtering with window size: {}'.format(window_size),'_'*20)

occupants_filtered_df = occupants_df.withColumns(conversion_dict)

if LOG:
    print('Median filtered dataset: ')
    occupants_filtered_df.show()
    print('_'*20, 'END: Median filtering with window size: {}'.format(window_size),'_'*20)



################################################## PCA TRAINING ###################################################
if TRAIN_PCA:

    no_occupants_url = NOISE_CSV_URL
    no_occupants_df = spark.read.csv(no_occupants_url, header=True,inferSchema=True) \
                                    .where("('2020-01-27' <= timestamp) AND (timestamp <='2020-02-04')")

    cols_to_process_ = no_occupants_df.columns.copy()
    cols_to_process_.remove('timestamp')

    assembler_nooccupants = VectorAssembler(inputCols = cols_to_process_, outputCol = 'features')
    windowSpec_ = Window.partitionBy("day_month_year").orderBy(asc("timestamp")).rowsBetween(-window_size//2, window_size//2) #Note: we can divide partition by hours to speed up computation
    conversion_dict_noise = {column: rolling_median_udf(F.collect_list(column).over(windowSpec_)) for column in cols_to_process}
    no_occupants_filtered_df = no_occupants_df.withColumn("day_month_year", concat(dayofmonth(col("timestamp")), month(col("timestamp")), year(col("timestamp"))))
    no_occupants_filtered_df = no_occupants_filtered_df.withColumns(conversion_dict_noise)

    assembled_df_no_occupants = assembler_nooccupants.transform(no_occupants_filtered_df)

    scaler = StandardScaler(inputCol="features", outputCol="scaled_features_centered", withStd=True, withMean=True)
    scaler = scaler.fit(assembled_df_no_occupants)
    assembled_df_no_occupants = scaler.transform(assembled_df_no_occupants) \
                                .drop("features") \
                                .withColumnRenamed("scaled_features_centered", "features")

    pca = PCA(k=9, inputCol="features", outputCol="pcaFeatures")

    if LOG:
        print('_'*20, 'START: noise PCA TRAINING','_'*20)

    pca = pca.fit(assembled_df_no_occupants)

    if LOG:
        print('_'*20, 'END: noise PCA TRAINING','_'*20)

    # Saving fitted PCA
    if not LOCAL:
        pca.save(NOISE_PCA_URL)

        if LOG:
            print('_'*20, 'noise PCAModel has been saved','_'*20)

################################################## PCA (NOISE) PROJECTION ###################################################

assembler = VectorAssembler(inputCols = cols_to_process, outputCol = 'features')
# importing pretrained PCA assuming similar sensors & sensor setup
if (not LOCAL) and (not TRAIN_PCA):
    if LOG:
        print('_'*20, 'Loading noise PCAModel from HDFS','_'*20)

    pca = PCAModel.load(NOISE_PCA_URL)

# applying PCA (noise) projection to dataset
n_components = 9
assembled_df_occupants = assembler.transform(occupants_filtered_df).orderBy('timestamp')
occupants_scaler = StandardScaler(inputCol="features", outputCol="scaled_features_centered", withStd=True, withMean=True)
occupants_scaler = occupants_scaler.fit(assembled_df_occupants)
assembled_df_occupants = occupants_scaler.transform(assembled_df_occupants) \
                            .drop("features") \
                            .withColumnRenamed("scaled_features_centered", "features")

# projecting features of occupant data into space generated by no occupant data
if LOG:
    print('_'*20, 'START: noise PCAModel inference','_'*20)

pca_occupants = pca.transform(assembled_df_occupants).orderBy('timestamp')
pca_occupants_unzipped = pca_occupants.withColumn("feature", vector_to_array("pcaFeatures")) \
                                        .select(['housing_unit']+['timestamp']+[col("feature")[i] for i in range(n_components)])

if LOG:
    print('Projected dataset: ')
    pca_occupants_unzipped.show()
    print('_'*20, 'END: noise PCAModel inference','_'*20)
#################################################### PCA NOISE REMOVAL ######################################################

if LOG:
    print('_'*20, 'START: noise removal (first PCA projected space component)','_'*20)

# zero-ing the first component of the pca, to remove it from re-projection in the original space. 
# Alternatively, we can just remove it and avoid going back to the original space
pca_occupants_unzipped = pca_occupants_unzipped.withColumn('feature[0]',lit(0))


# zipping vectors to a single colum
print(pca_occupants_unzipped.columns)
invert_columns_to_convert = pca_occupants_unzipped.columns
invert_columns_to_convert.remove('timestamp')
invert_columns_to_convert.remove('housing_unit')
assembler_invert = VectorAssembler(inputCols = invert_columns_to_convert, outputCol = 'pcaFeatures')

pca_occupants_zipped = assembler_invert.transform(pca_occupants_unzipped).orderBy('timestamp')

##FIXME SLOW PART
# reproject it to original space
K = pca.pc.toArray()
pca_occupants_features = pca_occupants_zipped.toPandas()
X = np.array(pca_occupants_features["pcaFeatures"].tolist())
pca_occupants_features = pca_occupants_features.drop(columns=["pcaFeatures"])
inv_transf_occupants = (X @ K.T)

# inverting normalization
inv_transf_occupants *= occupants_scaler.std 
inv_transf_occupants += np.array(occupants_scaler.mean)

inv_transf_occupants = spark.createDataFrame(pd.concat([pca_occupants_features,pd.DataFrame(inv_transf_occupants, columns=cols_to_process)], axis=1))

if LOG:
    print('Noise-removed dataset: ')
    inv_transf_occupants.show()
    print('_'*20, 'END: noise removal (first PCA projected space component)','_'*20)

'''
############################################### WINDOW-PCA + T-SQUARED LIMIT ################################################


################################################### EVENT HOURLY BINNING ####################################################


################################################## OUTPUT (SHOW) HEATMAP MATRIX / EVENTS DATAFRAME ####################################################

'''