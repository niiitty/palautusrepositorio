from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu


def test_tuomari_counts_wins_and_ties():
    tuomari = Tuomari()
    tuomari.kirjaa_siirto("k", "k")  # tie
    tuomari.kirjaa_siirto("k", "s")  # first wins
    tuomari.kirjaa_siirto("s", "k")  # second wins

    assert tuomari.tasapelit == 1
    assert tuomari.ekan_pisteet == 1
    assert tuomari.tokan_pisteet == 1


def test_voittaja_detects_first_to_five():
    tuomari = Tuomari()
    for _ in range(3):
        tuomari.kirjaa_siirto("k", "s")

    assert tuomari.voittaja() == 1
    assert tuomari.maksimi_pisteet() == 3


def test_tekoaly_cycles_moves_in_order():
    ai = Tekoaly()
    moves = [ai.anna_siirto() for _ in range(4)]

    # sequence should loop p -> s -> k -> p ...
    assert moves == ["p", "s", "k", "p"]


def test_tekoaly_parannettu_prefers_counter_move():
    ai = TekoalyParannettu(5)
    ai.aseta_siirto("k")
    ai.aseta_siirto("p")
    ai.aseta_siirto("p")

    # viimeisin_siirto = "p" and following move after another "p" should be countered with "s"
    assert ai.anna_siirto() == "s"
