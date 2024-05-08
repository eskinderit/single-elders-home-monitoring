from typing import Optional
import pandas as pd
# needed for pyspark windows installs
import findspark
findspark.init()

import numpy as np
import pyspark
from pyspark.ml.feature import PCA, StandardScaler

class PCAWrapper():
    """
    A wrapper class for PCA (Principal Component Analysis) using PySpark's implementation.

    Parameters:
        k (int, optional): Number of principal components to retain. Default is None.
        inputCol (str, optional): Input column name. Default is None.
        outputCol (str, optional): Output column name. Default is None.
        centering_data (bool): Whether to center the data before applying PCA. Default is True.
    """
    
    def __init__(self, *, 
               k: Optional[int] = None, 
               inputCol: Optional[str] = None,
               outputCol: Optional[str] = None, 
               centering_data: bool = True):

        # wrapping PySpark PCA implementation
        self.__PCA = PCA(k=k, inputCol=inputCol, outputCol=outputCol)

        self.__centering_data = centering_data
        self.__scaler = None

    def __getattr__(self, name):
        """
        Allows accessing attributes/methods of the wrapped PCA instance.
        """
        return getattr(self.__PCA, name)
    
    def getInputCol(self):
        return self.__PCA.getInputCol()

    def getOutputCol(self):
        return self.__PCA.getOutputCol()
    
    def fit(self, dataset: pyspark.sql.dataframe.DataFrame, params = None):
        """
        This methods performs two actions in sequence:
        
        1. Centers the data (remembering the means to re-apply during `transform()`) 
        2. Fits the PCA model to the input dataset.

        Parameters:
            dataset (pyspark.sql.dataframe.DataFrame): Input DataFrame.
            params: Additional parameters to be passed to the PCA model.

        Returns:
            PCAWrapper: The fitted PCA model.
        """
        
        if self.__centering_data:
            self.__scaler = StandardScaler(inputCol=self.getInputCol(), outputCol="scaled_features_centered", withStd=False, withMean=True)
            self.__scaler = self.__scaler.fit(dataset)
            centered_df = self.__scaler.transform(dataset)
            centered_df = centered_df.drop(self.getInputCol()).withColumnRenamed("scaled_features_centered", self.getInputCol())
            
            self.__PCA = self.__PCA.fit(centered_df, params)
            result = self.__PCA.transform(centered_df, params)

        else:
            self.__PCA = self.__PCA.fit(dataset, params)

        return self

    
    def transform(self, dataset: pyspark.sql.dataframe.DataFrame, params = None, use_actual_mean = False):
        """
        This methods performs two actions in sequence:
        1. Centers the data using the mean captured when calling `fit()`, unless `use_actual_mean` is set to True, in that case the mean on which `transform` is called is re-fitted.
        2. Transforms the input dataset using the fitted PCA model.

        Parameters:
            dataset (pyspark.sql.dataframe.DataFrame): Input DataFrame.
            params: Additional parameters to be passed to the PCA transformation.
            use_actual_mean (bool): Whether to use the actual mean for centering the data.

        Returns:
            pyspark.sql.dataframe.DataFrame: Transformed DataFrame.
        """
        
        if self.__centering_data:

            if use_actual_mean:
                self.__scaler = self.__scaler.fit(dataset)
                
            centered_df = self.__scaler.transform(dataset)
            centered_df = centered_df.drop(self.getInputCol()).withColumnRenamed("scaled_features_centered", self.getInputCol())
            
            return self.__PCA.transform(centered_df, params)
        else:
            return self.__PCA.transform(dataset, params)

    def inverse_transform(self, dataset: pyspark.sql.dataframe.DataFrame, schema=None):
        """
        Inverse transforms the dataset to the original space and re-adds the mean to invert the data-centering.

        Parameters:
            dataset (pyspark.sql.dataframe.DataFrame): Input DataFrame containing PCA transformed data.

        Returns:
            list: List of reprojected data.
        """
        
        # principal components matrix
        K = self.__PCA.pc.toArray()

        # inverting (by transposition) principal component matrix
        K_T = K.T

        pd_dataset = dataset.toPandas()
        
        X = np.array(pd_dataset[self.getOutputCol()].tolist())

        if self.__centering_data:
            reprojected_dataset = X@K.T + np.array(self.__scaler.mean)

        else:
            reprojected_dataset = X@K.T
            
        return pd.concat([pd_dataset,pd.DataFrame(reprojected_dataset, columns=schema)], axis=1)