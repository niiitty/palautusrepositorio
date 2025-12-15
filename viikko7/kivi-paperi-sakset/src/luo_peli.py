from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly

class LuoPeli:
    @staticmethod
    def luo_peli(tyyppi):
        peli = LuoPeli._hae_peli(tyyppi)

        if not peli:
            return None

        print(
            "Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s"
        )

        peli.pelaa()
        return True

    @staticmethod
    def _hae_peli(tyyppi):
        if tyyppi.endswith("a"):
            return KPSPelaajaVsPelaaja()
        elif tyyppi.endswith("b"):
            return KPSTekoaly()
        elif tyyppi.endswith("c"):
            return KPSParempiTekoaly()

        return None
