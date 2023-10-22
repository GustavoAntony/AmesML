import joblib
import numpy as np
import pickle
import pathlib
import pandas as pd
from sklearn.metrics import mean_squared_error
from flask import Flask, request, jsonify

DATA_DIR = pathlib.Path.cwd().parent/ 'AmesML' / 'data'
API_DIR = pathlib.Path.cwd() / 'api'
clean_data_path = DATA_DIR / 'processed' / 'ames_clean.pkl'
with open(clean_data_path, 'rb') as file:
    data = pickle.load(file)

DATA = data.copy()
RIDGE = joblib.load(f'{API_DIR}/ridge_model.pkl')

def Mytransformations(data):
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
    return model_data

# Crie uma instância do aplicativo Flask
app = Flask(__name__)

# Defina uma rota para a página inicial
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Rota que recebe um JSON e retorna um texto
@app.route('/predict', methods=['POST'])
def json_to_text():
    try:
        # Recebe o JSON da solicitação GET
        row = request.get_json()
        row = pd.DataFrame(row, index=[0])
        data = pd.concat([DATA, row], axis=0)
        # Verifica se o JSON contém a chave 'mensagem'
        print(DATA.shape)
        data = Mytransformations(DATA)
        print(data.shape)
        input = data.iloc[-1]
        print(input.head())
        resposta = input['SalePrice'].copy()
        input = input.drop('SalePrice')
        print(input.shape)
        input = input.values.reshape(1, -1)
        predito = RIDGE.predict(input)


        
        return f'Predito: {predito[0]}, real: {resposta}', 200
    except Exception as e:
        return f'Ocorreu um erro: {str(e)}', 500  # Código de status 500 para erros internos


# Execute o aplicativo na porta 5000
if __name__ == '__main__':
    app.run()

# ridge = joblib.load('../ridge_model.pkl')
# ridge_pred = ridge.predict(Xtest)
