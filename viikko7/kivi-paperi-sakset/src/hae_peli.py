from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly

def hae_peli(syote):
    if syote.endswith("a"):
        return KPSPelaajaVsPelaaja()
    elif syote.endswith("b"):
        return KPSTekoaly()
    elif syote.endswith("c"):
        return KPSParempiTekoaly()

    return None