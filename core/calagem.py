# core/calagem.py

def calcular_necessidade_calagem(v_desejado, v_atual, ctc, prnt):
    """
    Calcula a necessidade de calcário (t/ha).
    Fórmula: ((Vd - Va) * CTC * profundidade * densidade) / (100 * PRNT)
    Para simplificação, consideramos profundidade e densidade embutidas em CTC.
    """

    necessidade = ((v_desejado - v_atual) * ctc) / (100 * prnt)
    return max(necessidade, 0)
