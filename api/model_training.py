from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
import pathlib
import pandas as pd
import joblib


DATA_DIR = pathlib.Path.cwd().parent/ 'AmesML' / 'data'
clean_data_path = DATA_DIR / 'processed' / 'ames_clean.pkl'
with open(clean_data_path, 'rb') as file:
    data = pickle.load(file)

print(data.shape)
model_data = data.copy()
categorical_columns = []
ordinal_columns = []
for col in model_data.select_dtypes('category').columns:
    if model_data[col].cat.ordered:
        ordinal_columns.append(col)
    else:
        categorical_columns.append(col)

for col in ordinal_columns:
    codes, _ = pd.factorize(data[col], sort=True)
    model_data[col] = codes

model_data = pd.get_dummies(model_data, drop_first=True)

for cat in categorical_columns:
    dummies = []
    for col in model_data.columns:
        if col.startswith(cat + "_"):
            dummies.append(f'"{col}"')
    dummies_str = ', '.join(dummies)


#salvando os dados em um arquivo pickle
with open(DATA_DIR / 'processed' / 'ames_model_data.pkl', 'wb') as file:
    pickle.dump(model_data, file)

X = model_data.drop(columns=['SalePrice']).copy()
y = model_data['SalePrice'].copy()
print(X.shape, y.shape)
RANDOM_SEED = 42
# Vamos procurar os melhores parâmetros para o Ridge

grid_search = GridSearchCV(
    Ridge(random_state=RANDOM_SEED),
    {'alpha': [0.01, 0.1, 1, 10, 100]},
    cv=4,
    n_jobs=-1,
    scoring='neg_mean_squared_error',
    return_train_score=True
)

grid_search.fit(X, y)

# Vamos adotar o melhor regressor, ou seja, o RandomForestRegressor com os melhores hiperparâmetros.
ridge = grid_search.best_estimator_

joblib.dump(ridge, 'ridge_model.pkl')


