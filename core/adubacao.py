# core/adubacao.py

def recomendar_n(produtividade, tabela_n):
    """
    Recomendação de Nitrogênio (kg/ha) com base na produtividade esperada.
    tabela_n: dict {produtividade_max: dose}
    """
    for prod_max, dose in sorted(tabela_n.items()):
        if produtividade <= int(prod_max):
            return dose
    return max(tabela_n.values())

def recomendar_p(p_mehlich, faixas_p):
    """
    Recomenda dose de P2O5 (kg/ha) conforme teor de P extraído com Mehlich-1.
    faixas_p: lista de listas [[max_teor, dose], ...]
    """
    for max_p, dose in faixas_p:
        if p_mehlich <= max_p:
            return dose
    return 0

def recomendar_k(ca, mg, k, faixas_sat_k):
    """
    Recomenda dose de K2O (kg/ha) conforme saturação por K (%).
    faixas_sat_k: lista de listas [[max_sat, dose], ...]
    """
    sb = ca + mg + k
    if sb == 0:
        return 0
    sat_k = (k / sb) * 100
    for max_sat, dose in faixas_sat_k:
        if sat_k <= max_sat:
            return dose
    return 0
