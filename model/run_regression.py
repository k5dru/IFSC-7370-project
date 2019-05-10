import pandas as pd
from sqlalchemy import create_engine

import os
import sys
from auto_ml import Predictor
from auto_ml.utils import get_boston_dataset
from sklearn.model_selection import train_test_split

try: 
    df = pd.read_csv('cache_of_model_intput.tmp')
except: 
    with open('regression_query.sql', 'r') as file:
        query = file.read()
    engine = create_engine('postgresql:///lemley') # https://stackoverflow.com/questions/23839656/sqlalchemy-no-password-supplied-error
    df = pd.read_sql(query ,con=engine)
    # cache the df as a local file for speedy repeated runs
    df.to_csv('cache_of_model_intput.tmp', index=False)

df=df.drop(columns=["intervalbegin", "spp_price_event_flag"])
timecol = pd.to_datetime(df['time_utc'])
df['time_utc'] = timecol
df = df.set_index('time_utc')

df_train, df_test = train_test_split(df, test_size=0.20, shuffle=False)

print ("Training set: (" + str(len(df_train.index)) +  ")" )
print (df_train.head()) 

print ("Testing set:  (" + str(len(df_test.index)) +  ")" )
print (df_test.head()) 


try:
    last_output = pd.read_csv('cache_of_regression_output.csv')
    df_test = last_output
except: 
    column_descriptions = {
        'lmp': 'output', 
        'time_utc' : 'ignore'
            }

    ml_predictor = Predictor(type_of_estimator='regressor', column_descriptions=column_descriptions)
    # ml_predictor.train(df_train, model_names=['DeepLearningRegressor']) 
    ml_predictor.train(df_train) # just use gradient-boosted regressor instead of tensorflow

    ml_predictor.score(df_test, df_test.lmp)

    predictions = ml_predictor.predict(df_test)
    df_test['PredictedLMP'] = predictions

    df_test.to_csv('cache_of_regression_output.csv', columns = ['time_utc', 'lmp', 'PredictedLMP'])

# trying to follow this here: https://www.dataquest.io/blog/tutorial-time-series-analysis-with-pandas/
import seaborn as sns
import matplotlib.pyplot as plt
# Use seaborn style defaults and set the default figure size

# sns.set(rc={'figure.figsize':(11, 4)})
# ax = df_test['PredictedLMP'].plot(linewidth=0.5, label='LMP')
# ax.set_ylabel('Actual vs. Predicted LMP')
# plt.show()

# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(15, 6)})

# from the page exactly, almost: 
# Plot daily and weekly resampled time series together
fig, ax = plt.subplots()
ax.plot(df_test['lmp'], marker='.', linestyle='-', linewidth=0.5, label='LMP')
ax.plot(df_test['PredictedLMP'], marker='.', linestyle='-', linewidth=0.5, label='Predicted LMP')
ax.set_ylabel('Actual vs. Predicted LMP')
ax.legend();
plt.show()

sys.exit(0)
