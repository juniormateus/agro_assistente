# services/openai_api.py
import os

def gerar_interpretacao_openai(dados_entrada, resultados):
    """
    (Não funcional ainda - placeholder)
    Esta função futuramente vai se conectar com a API da OpenAI
    e gerar um texto interpretativo com base nos resultados de calagem e adubação.
    """
    prompt = f"""
    Você é um agrônomo. Abaixo está uma análise de solo e as recomendações obtidas:

    🔍 Análise de Solo:
    Ca: {dados_entrada['ca']} cmolc/dm³
    Mg: {dados_entrada['mg']} cmolc/dm³
    K: {dados_entrada['k']} cmolc/dm³
    Al: {dados_entrada['al']} cmolc/dm³
    P: {dados_entrada['p']} mg/dm³

    🎯 Recomendação:
    Calagem: {resultados['calagem']} t/ha
    N: {resultados['n']} kg/ha
    P₂O₅: {resultados['p2o5']} kg/ha
    K₂O: {resultados['k2o']} kg/ha

    Gere uma interpretação técnica e recomendação de manejo para o produtor.
    """

    return "⚠️ Integração com OpenAI ainda não habilitada."
