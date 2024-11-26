from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return "A API da Magazine Luiza está no ar"

@app.route('/pegardados/')
def categoria():
    dados = pd.read_csv('../1_bases_tratadas/base_magalu.csv', sep=';', encoding='utf-8-sig')
    moveis = dados[dados['Tipo'] == 'Móvel']
    total_moveis = moveis['Preço Bruto'].sum()
    resposta = {'total_moveis': total_moveis}
    return jsonify(resposta)


@app.route('/tabela/')
def tabela():
    try:
        dados = pd.read_csv('../1_bases_tratadas/base_magalu.csv', sep=';', encoding='utf-8-sig')
        if 'Unnamed: 0' in dados.columns:
            dados = dados.drop('Unnamed: 0', axis=1)
        dados_json = dados.to_json(orient='records', force_ascii=False)
        return dados_json, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    
app.run(debug=True)

