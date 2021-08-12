import shutil
import numpy as np
import pandas as pd

# Handling missing data using-
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer
 
# Handling non-numeric data using-
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder 

import os
import yaml
from yaml.loader import FullLoader
from scipy import stats

class Preprocess:     
    def manual_preprocess(self,config, folderLocation):
        """
        This function is for preprocessing the data when the user selects manual preprocessing.                     
        """
        with open(config) as f:
            config_data= yaml.load(f,Loader=FullLoader) 

        df = pd.read_csv(config_data["raw_data_address"])
        df.dropna(how='all', axis=1, inplace=True)

        label_list = []
        if config_data["is_auto_preprocess"] == False:

            if config_data['drop_column_name'] != []:
                del config_data['drop_column_name'][0]
                for column in config_data['drop_column_name']:
                    if column != config_data['target_column_name']:
                        df=df.drop(column, axis = 1)
                    else:
                        del config_data['drop_column_name'][0]


            if config_data['imputation_column_name'] != []:
                del config_data['imputation_column_name'][0]
                del config_data['impution_type'][0]
                strategy_values_list = []

                for index, column in enumerate(config_data["imputation_column_name"]):
                    if df[column].dtype == object:
                        impution_type = "most_frequent"
                        config_data["impution_type"][index] = "most_frequent"
                    else:
                        impution_type = config_data["impution_type"][index] 

                    if impution_type == "mean":
                        df_value = df[[column]].values
                        imputer = SimpleImputer(missing_values = np.nan, strategy = "mean")
                        strategy_values_list.append(df[column].mean())
                        df[[column]] = imputer.fit_transform(df_value)

                    elif impution_type == "median":
                        df_value = df[[column]].values
                        imputer = SimpleImputer(missing_values =  np.nan, strategy = "median")
                        strategy_values_list.append(df[column].median())
                        df[[column]] = imputer.fit_transform(df_value)

                    elif impution_type == "most_frequent":
                        df.fillna(df.select_dtypes(include='object').mode().iloc[0], inplace=True)
                        strategy_values_list.append(df[column].value_counts().idxmax())

                    elif impution_type=='knn':
                        df_value = df[[column]].values
                        imputer = KNNImputer(n_neighbors = 4, weights = "uniform",missing_values =  np.nan)
                        strategy_values_list.append(0)
                        df[[column]] = imputer.fit_transform(df_value)

                if strategy_values_list != []:
                    config_data['mean_median_mode_values'] = list(map(str, strategy_values_list))    
            

            if config_data['scaling_column_name'] != []:
                del config_data['scaling_column_name'][0]
                del config_data['scaling_type'][0]
                scaled_value_list = []
                for index, column in enumerate(config_data["scaling_column_name"]):
                    if df[column].dtype == object or config_data["target_column_name"] == column:
                        del config_data['scaling_column_name'][index]
                        del config_data['scaling_type'][index]
                        pass
                    else:
                        scaling_type = config_data["scaling_type"][index]
                        config_data['scaling_values'] = {}
                        df_value = df[[column]].values
                        df_std = (df_value - df_value.min(axis=0)) / (df_value.max(axis=0) - df_value.min(axis=0))

                        if scaling_type == "normalization":
                            scaled_value = df_std
                            scaled_value_list.append({"min":float(df_value.min(axis=0)),"max":float(df_value.max(axis=0))})

                        elif scaling_type == 'standarization':
                            scaled_value = (df_value - df_value.mean()) / df_std 
                            scaled_value_list.append({"min":float(df_value.min(axis=0)),"max":float(df_value.max(axis=0)),"mean":float(df_value.mean())})

                        config_data['scaling_values'] = scaled_value_list
                        df[[column]] = scaled_value


            if config_data['encode_column_name'][0] != []:
                del config_data['encode_column_name'][0]
                del config_data['encoding_type'][0]
                

                for index, column in enumerate(config_data["encode_column_name"]):
                    encoding_type = config_data["encoding_type"][index]

                    if(df[column].dtype == 'object') and (df[column].nunique() > 30) and (config_data["target_column_name"] != column):
                        df.drop(column, axis = 1,inplace=True)
                        del config_data['encode_column_name'][index]
                        del config_data['encoding_type'][index]

                    elif config_data["target_column_name"] == column and df[column].dtype == 'object':
                        config_data["encoding_type"][index] = "Label Encoding"
                        encoding_type == "Label Encoding"

                    elif config_data["target_column_name"] == column and df[column].dtype != 'object':
                        del config_data['encode_column_name'][index]
                        del config_data['encoding_type'][index]
                        pass

                    elif df[column].dtype != 'object'and df[column].nunique() > 30:
                        del config_data['encode_column_name'][0]
                        del config_data['encoding_type'][0]
                        pass

                    elif encoding_type == "Label Encoding":
                        df[column].astype(str)
                        encoder = LabelEncoder()
                        df[column] = encoder.fit_transform(df[column])
                        key = list(map(str,encoder.classes_.tolist()))
                        label_list.append({column : dict(zip(key, range(len(key))))})
                        config_data['labels'] = label_list

                    elif encoding_type == "One-Hot Encoding":
                        encoder = OneHotEncoder(sparse=False)
                        df_encoded = pd.DataFrame (encoder.fit_transform(df[[column]]))
                        df_encoded.columns = encoder.get_feature_names([column])
                        df.drop([column] ,axis=1, inplace=True)
                        df= pd.concat([df, df_encoded ], axis=1)
        

        ### Default
        df.fillna(df.dtypes.replace({'float64': 0.0, 'O': 'NULL'}), downcast='infer', inplace=True)
        for column in df.columns:
            if df[column].dtype == 'object'and df[column].nunique() > 30 and config_data["target_column_name"] != column:
                df.drop(column, axis = 1,inplace=True)
                config_data['drop_column_name'].extend([column])

        if df[config_data["target_column_name"]].dtype == 'object':
            column=config_data["target_column_name"]
            df[column].astype(str)
            encoder = LabelEncoder()
            df[column] = encoder.fit_transform(df[column])
            key = list(map(str,encoder.classes_.tolist()))
            label_list.append({column : dict(zip(key, range(len(key))))})
            config_data['labels'] = label_list

        object_type_column_list = []
        for column in df.columns:
            if df[column].dtype == 'object':
                object_type_column_list.append(column)
                config_data['encode_column_name'].extend([column])
                config_data['encoding_type'].extend(['One-Hot Encoding'])

        if object_type_column_list != []:
            for column in object_type_column_list:
                encoder = OneHotEncoder(sparse=False)
                df_encoded = pd.DataFrame (encoder.fit_transform(df[[column]]))
                df_encoded.columns = encoder.get_feature_names([column])
                df.drop([column] ,axis=1, inplace=True)
                df= pd.concat([df, df_encoded ], axis=1)
                
        

        # if config_data["Remove_outlier"] == True:
        #     z = np.abs(stats.zscore(df))
        #     df = df[(z < 3).all(axis=1)]
            

        # if config_data["feature_selection"] == True:
        #     col_corr = set()
        #     corr_matrix = df.corr()
        #     for i in range(len(corr_matrix.columns)):
        #             for j in range(i):
        #                 if abs(corr_matrix.iloc[i, j]) > 0.90:
        #                     col_corr.add(corr_matrix.columns[i])
        #     df = df.drop(col_corr,axis=1)
        #     config_data['corr_col'] = list(col_corr)
        
        config_data['final_columns']=list(df.columns)
                        
        df.to_csv('clean_data.csv')
        shutil.move("clean_data.csv",folderLocation)
        clean_data_address = os.path.abspath(os.path.join(folderLocation,"clean_data.csv"))
        config_data['clean_data_address'] = clean_data_address

        with open(config, 'w') as yaml_file:
            yaml_file.write( yaml.dump(config_data, default_flow_style=False))
        
        return clean_data_address
