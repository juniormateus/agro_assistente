def volume_calda(volume_ha, area_tratada):
    """
    Calcula o volume total de calda a ser aplicado, em litros.

    Parâmetros:
    - volume_ha: Volume de calda por hectare (L/ha)
    - area_tratada: Área total a ser tratada (ha)

    Retorna:
    - Volume total da calda (L)
    """
    return volume_ha * area_tratada


def dose_produto(dose_recomendada, area_tratada):
    """
    Calcula a dose total de produto    
    Parâmetros:
    - Dose recomendada (por ha)
    - Área tratada (ha)

    Retorna:
    - Dose total de produto (em mL ou g)
    """
    return dose_recomendada * area_tratada

def dose_tanque(dose_recomendada, volume_tanque, volume_aplicacao):
    """
    Calcula a dose por tanque para caso trabalhe por pulverizador e não área total.

    Parâmetros:
    - Dose recomendada (L/ha ou g/ha)
    - Volume do tanque (L)
    - Volume de aplicação por ha (L/ha)

    Retorna:
    - Dose no tanque (mL ou g)
    """
    return (dose_recomendada * volume_tanque) / volume_aplicacao