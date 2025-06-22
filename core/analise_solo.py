# core/analise_solo.py

def calcular_ctc(ca, mg, k, al):
    """
    Calcula a Capacidade de Troca de Cátions (CTC) em cmolc/dm³.
    """
    return ca + mg + k + al

def calcular_saturacao_bases(ca, mg, k, al):
    """
    Calcula a saturação por bases (V%) do solo.
    V% = (SB/CTC)*100, onde SB = soma de bases (Ca + Mg + K).
    """
    ctc = calcular_ctc(ca, mg, k, al)
    sb = ca + mg + k
    if ctc == 0:
        return 0
    return (sb / ctc) * 100
