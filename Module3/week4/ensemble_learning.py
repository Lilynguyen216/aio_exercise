# -*- coding: utf-8 -*-
"""Ensemble_learning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19xms9_5sTUna5c03z1G_0a8BBgkj4VAY
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

!gdown 1qeJqFtRdjjHqExbWJcgKy0yJbczTTAE3
# https://drive.google.com/file/d/1qeJqFtRdjjHqExbWJcgKy0yJbczTTAE3/view?usp=drivesdk

dataset_path = '/content/Housing.csv'
df = pd.read_csv(dataset_path)
df.head()

categorical_cols = df.select_dtypes(include=['object']).columns.to_list()

ordinal_encoder = OrdinalEncoder()
encoded_categorical_cols = ordinal_encoder.fit_transform(df[categorical_cols])

encoded_categorical_df = pd.DataFrame(
    encoded_categorical_cols,
    columns=categorical_cols
)
numerical_df = df.drop(columns=categorical_cols, axis = 1)
numerical_df.head()

encoded_df = pd.concat([numerical_df, encoded_categorical_df], axis=1)
encoded_df.head()

normalizer = StandardScaler()
dataset_arr = normalizer.fit_transform(encoded_df)
print(dataset_arr.shape)
dataset_arr

# Init X, y
X, y = dataset_arr[:, 1:], dataset_arr[:, 0]

test_size = 0.3
random_state = 1
is_shuffle = True

# Splitting the dataset
X_train, X_val, y_train, y_val = train_test_split(
    X, y,
    test_size=test_size,
    random_state=random_state,
    shuffle=is_shuffle
)

regressor = RandomForestRegressor(
    random_state=random_state
)
regressor.fit(X_train, y_train)

regressor = AdaBoostRegressor(
    random_state=random_state
)
regressor.fit(X_train, y_train)

regressor = GradientBoostingRegressor(
    random_state=random_state
)
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_val)

mae = mean_absolute_error(y_val, y_pred)
mse = mean_squared_error(y_val, y_pred)
print(f'MAE: {mae}')
print(f'MSE: {mse}')