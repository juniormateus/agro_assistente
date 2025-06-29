# core/conversor.py

def converter_volume(valor: float, de: str, para: str) -> float:
    fatores = {
        "ml": 1,
        "l": 1000,
        "m3": 1_000_000,
        "gal_us": 3785.41,
        "gal_uk": 4546.09,
    }
    return valor * fatores[de] / fatores[para]


def converter_peso(valor: float, de: str, para: str) -> float:
    fatores = {
        "g": 1,
        "kg": 1000,
        "t": 1_000_000,
        "arroba": 15000,
        "saca60": 60000,
        "lb": 453.592,
    }
    return valor * fatores[de] / fatores[para]


def converter_area(valor: float, de: str, para: str) -> float:
    fatores = {
        "m2": 1,
        "ha": 10_000,
        "alqueire_sp": 24_200,
        "alqueire_mg": 48_400,
        "acre": 4046.86,
    }
    return valor * fatores[de] / fatores[para]


def converter_temperatura(valor: float, de: str, para: str) -> float:
    if de == para:
        return valor
    elif de == "c" and para == "f":
        return (valor * 9/5) + 32
    elif de == "f" and para == "c":
        return (valor - 32) * 5/9
    else:
        raise ValueError("Conversão de temperatura inválida.")
