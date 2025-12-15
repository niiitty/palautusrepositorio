def test_root_page_renders(client):
    resp = client.get("/")
    assert resp.status_code == 200
    content = resp.data.decode()
    assert "Pelitilanne:" in content
    assert "Viimeisin:" in content


def test_ai_game_flow_persists_session(client):
    # first round vs easy AI
    resp1 = client.post("/pelaa", data={"mode": "b", "siirto1": "k"})
    assert resp1.status_code == 200
    text1 = resp1.data.decode()
    assert "Pelitilanne: 0 - 1" in text1  # AI opens with "p"

    # second round continues same session, AI cycles to "s"
    resp2 = client.post("/pelaa", data={"mode": "b", "siirto1": "k"})
    assert resp2.status_code == 200
    text2 = resp2.data.decode()
    assert "Pelitilanne: 1 - 1" in text2


def test_invalid_move_in_two_player_shows_error(client):
    resp = client.post("/pelaa", data={"mode": "a", "siirto1": "x", "siirto2": "k"})
    assert resp.status_code == 200
    content = resp.data.decode()
    assert "Syötä k/p/s" in content


def test_game_stops_after_three_wins(client):
    # First player wins three times in a row in two-player mode
    for _ in range(3):
        resp = client.post("/pelaa", data={"mode": "a", "siirto1": "k", "siirto2": "s"})
        assert resp.status_code == 200

    content = resp.data.decode()
    assert "Pelitilanne: 3 - 0" in content
    assert "Ottelu päättyi" in content

    # Further moves are ignored and game is locked
    resp2 = client.post("/pelaa", data={"mode": "a", "siirto1": "k", "siirto2": "s"})
    assert resp2.status_code == 200
    locked = resp2.data.decode()
    assert "Pelitilanne: 3 - 0" in locked
    assert "Ottelu on jo päättynyt" in locked


def test_reset_clears_scores(client):
    # play once to change score
    client.post("/pelaa", data={"mode": "a", "siirto1": "k", "siirto2": "s"})

    resp = client.post("/reset", data={"mode": "a"})
    assert resp.status_code == 200
    content = resp.data.decode()
    assert "Pelitilanne: 0 - 0" in content
    assert "Tulokset nollattu" in content
