# Modelo Ridge
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
import pickle
import pathlib

RANDOM_SEED = 42

DATA_DIR = pathlib.Path.cwd().parent / 'data'
clean_data_path = DATA_DIR / 'processed' / 'ames_clean.pkl'
with open(clean_data_path, 'rb') as file:
    data = pickle.load(file)

# Vamos procurar os melhores parâmetros para o Ridge

grid_search = GridSearchCV(
    Ridge(random_state=RANDOM_SEED),
    {'alpha': [0.01, 0.1, 1, 10, 100]},
    cv=4,
    n_jobs=-1,
    scoring='neg_mean_squared_error',
    return_train_score=True
)

# grid_search.fit(Xtrain, ytrain)

# # Vamos adotar o melhor regressor, ou seja, o RandomForestRegressor com os melhores hiperparâmetros.
# ridge = grid_search.best_estimator_

# # Agora vamos medir o desempenho deste regressor com validação cruzada.
# ridge_scores = cross_val_score(ridge, Xtrain, ytrain, 
#                                     scoring="neg_mean_squared_error", cv=10, n_jobs=-1)

# ridge_rmse_scores = np.sqrt(-ridge_scores)

# ridge_coeficientes = ridge.coef_

# plot_importances(data_columns, ridge_coeficientes)