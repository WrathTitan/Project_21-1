import shutil
import numpy as np
import pandas as pd

# Handling missing data using-
from sklearn.impute import KNNImputer

# Handling non-numeric data using-
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder 

from yaml.loader import FullLoader
import os
import yaml
from scipy import stats
import random

class InferencePreprocess:     
    def inference_preprocess(self,config,folderLocation,inference_data_address):

        with open(config) as f:
            config_data= yaml.load(f,Loader=FullLoader) 
  
        df = pd.read_csv(inference_data_address)
        
        df.dropna(how='all', axis=1, inplace=True)

        
        df.fillna(df.dtypes.replace({'float64': 0.0, 'O': 'NULL'}), downcast='infer', inplace=True)

        if config_data['drop_column_name']!=[] and config_data['drop_column_name'][0] == '':
            del config_data['drop_column_name'][0]
            
        if config_data['drop_column_name'] != []:
            df=df.drop(config_data["drop_column_name"], axis = 1)
                

        if config_data['imputation_column_name'] != [] and config_data['imputation_column_name'][0] == '':
            del config_data['imputation_column_name'][0]
        
        if config_data['imputation_column_name']!= []:
            for index, column in enumerate(config_data["imputation_column_name"]):
                if column not in config_data['drop_column_name']:
                    if config_data["impution_type"][index] =='knn':
                        df_value = df[[column]].values
                        imputer = KNNImputer(n_neighbors = 4, weights = "uniform",missing_values = np.nan)
                        df[[column]] = imputer.fit_transform(df_value)

                    elif config_data["impution_type"][index] != 'knn':
                        replace_value = config_data["mean_median_mode_values"][index] 
                        df[column].replace(to_replace = np.nan, value = replace_value)
        
        if config_data['scaling_column_name']!=[] and config_data['scaling_column_name'][0] == '':
            del config_data['scaling_column_name'][0]
            
        if config_data['scaling_column_name']!= []:
            for index, column in enumerate(config_data["scaling_column_name"]):
                if column not in config_data['drop_column_name']:
                    scaling_type = config_data["scaling_type"][index]                
                    df_value = df[[column]].values

                    if scaling_type == "normalization":
                        mi = config_data['scaling_values'][index]['min']
                        ma = config_data['scaling_values'][index]['max']
                        df_std = (df_value - mi) / (ma - mi)
                        scaled_value = df_std * (1 - 0)

                    elif scaling_type == 'standarization':
                        mi = config_data['scaling_values'][index]['min']
                        mean = config_data['scaling_values'][index]['mean']
                        ma = config_data['scaling_values'][index]['max']
                        df_std = (df_value - mi) / (ma - mi)
                        scaled_value = (df_value - mean) / df_std 

                    df[[column]] = scaled_value
            
        if config_data['encode_column_name']!=[] and  config_data['encode_column_name'][0] == '':
            del config_data['encode_column_name'][0]
            del config_data['encoding_type'][0]

        if config_data['encode_column_name'] != []:
            for index, column in enumerate(config_data["encode_column_name"]):
                if column not in config_data['drop_column_name'] and column != config_data['target_column_name']:
                    encoding_type = config_data["encoding_type"][index]
                    
                    
                    if encoding_type == "Label Encoding":
                        for i in range(len(config_data['labels'])):
                            df[column].astype(str)
                            label = config_data['labels'][i]
                            df = df.replace(label)

                    elif encoding_type == "One-Hot Encoding":
                        encoder = OneHotEncoder(sparse=False)
                        df_encoded = pd.DataFrame (encoder.fit_transform(df[[column]]))
                        df_encoded.columns = encoder.get_feature_names([column])
                        df.drop([column] ,axis=1, inplace=True)
                        df= pd.concat([df, df_encoded ], axis=1)
                    
 
        # if config_data['encode_column_name'][0] == '':
        #     del config_data['encode_column_name'][0]
        
        # if config_data['encode_column_name'] != []:
        #     df=df.drop(config_data["corr_col"], axis = 1)
        col_names=list(df.columns)
        orig_col_names=config_data["final_columns"]
        new_col=list(set(orig_col_names)-set(col_names))
        print(new_col)
        df[new_col]=0

        if config_data['target_column_name'] in df.columns:
            df=df.drop(config_data["target_column_name"], axis = 1)
            
        ran=random.randint(100,999)
        df.to_csv('inference_clean_data'+str(ran)+'.csv')
        shutil.move('inference_clean_data'+str(ran)+'.csv',folderLocation)
        inference_clean_data_address = os.path.abspath(os.path.join(folderLocation,'inference_clean_data'+str(ran)+'.csv'))
        config_data['inference_clean_data_address'] = inference_clean_data_address

        with open(config, 'w') as yaml_file:
            yaml_file.write( yaml.dump(config_data, default_flow_style=False))
        
        return inference_clean_data_address