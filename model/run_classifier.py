import pandas as pd
from sqlalchemy import create_engine

import os

from auto_ml import Predictor
from auto_ml.utils import get_boston_dataset
from sklearn.model_selection import train_test_split

try: 
    df = pd.read_csv('cache_of_model_intput.tmp')
except: 
    with open('classifier_query.sql', 'r') as file:
        query = file.read()
    engine = create_engine('postgresql:///lemley') # https://stackoverflow.com/questions/23839656/sqlalchemy-no-password-supplied-error
    df = pd.read_sql(query ,con=engine)
    # cache the df as a local file for speedy repeated runs
    df.to_csv('cache_of_model_intput.tmp')

df=df.drop(columns=["intervalbegin", "time_utc", "lmp"])

df_train, df_test = train_test_split(df, test_size=0.25, shuffle=False)
df_feature, df_test = train_test_split(df_test, test_size=0.5, shuffle=False)

print ("Training set: (" + str(len(df_train.index)) +  ")" )
print (df_train.head()) 

print ("Feature learning set: (" + str(len(df_feature.index)) +  ")" )
print (df_feature.head()) 

print ("Testing set:  (" + str(len(df_test.index)) +  ")" )
print (df_test.head()) 


column_descriptions = {
    'spp_price_event_flag': 'output'
        }

ml_predictor = Predictor(type_of_estimator='classifier', column_descriptions=column_descriptions)
# ml_predictor = Predictor(type_of_estimator='regressor', column_descriptions=column_descriptions)

# ml_predictor.train(df_train)
ml_predictor.train(df_train, feature_learning=True, fl_data=df_feature) #  see https://auto-ml.readthedocs.io/en/latest/deep_learning.html 
# ml_predictor.train(df_train, model_names=['DeepLearningClassifier']) #  see https://auto-ml.readthedocs.io/en/latest/deep_learning.html 

ml_predictor.score(df_test, df_test.spp_price_event_flag)


