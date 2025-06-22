# core/utils.py

def validar_parametros_entrada(**kwargs):
    """
    Valida os parâmetros de entrada básicos para análise do solo.
    Pode ser expandido para verificar tipos, valores mínimos e máximos.
    """
    for nome, valor in kwargs.items():
        if valor is None:
            raise ValueError(f"Parâmetro {nome} não pode ser None")
        if not isinstance(valor, (int, float)):
            raise TypeError(f"Parâmetro {nome} deve ser numérico")
        if valor < 0:
            raise ValueError(f"Parâmetro {nome} não pode ser negativo")

def formatar_resultados(calagem, n, p2o5, k2o):
    """
    Formata os resultados para exibição.
    """
    return {
        "calagem_t_ha": round(calagem, 2),
        "nitrogenio_kg_ha": n,
        "fosforo_p2o5_kg_ha": p2o5,
        "potassio_k2o_kg_ha": k2o
    }
