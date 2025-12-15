from uuid import uuid4
from flask import Flask, request, make_response, redirect, render_template_string
from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu

app = Flask(__name__)

_ALLOWED = {"k", "p", "s"}


class _PeliIstunto:
    def __init__(self, tila):
        self.tila = tila  # "a" (pvp), "b" (ai), "c" (hard ai)
        self.tuomari = Tuomari()
        self.ai = self._luo_ai(tila)
        self.viimeisin = None  # (eka, toka, selite)

    @staticmethod
    def _luo_ai(tila):
        if tila == "b":
            return Tekoaly()
        if tila == "c":
            return TekoalyParannettu(10)
        return None

    def nollaa(self, tila):
        self.__init__(tila)


_ISTUNNOT = {}


def _hae_istunto(session_id, tila):
    istunto = _ISTUNNOT.get(session_id)
    if not istunto:
        istunto = _PeliIstunto(tila)
        _ISTUNNOT[session_id] = istunto
    elif istunto.tila != tila:
        istunto.nollaa(tila)
    return istunto


def _analysoi_siirrot(eka, toka):
    if eka == toka:
        return "Tasapeli"
    if (eka, toka) in (("k", "s"), ("s", "p"), ("p", "k")):
        return "Eka voittaa"
    return "Toka voittaa"


def _renderoi(istunto, viesti=None):
    scoreboard = f"Pelitilanne: {istunto.tuomari.ekan_pisteet} - {istunto.tuomari.tokan_pisteet}"\
                 f" | Tasapelit: {istunto.tuomari.tasapelit}"
    viimeisin = "-" if not istunto.viimeisin else f"{istunto.viimeisin[0]} vs {istunto.viimeisin[1]} → {istunto.viimeisin[2]}"
    voittaja = istunto.tuomari.voittaja()
    if voittaja:
        viesti = viesti or ("Ottelu päättyi – voittaja: " + ("Ensimmäinen" if voittaja == 1 else "Toinen"))

    html = render_template_string(
        _TEMPLATE,
        tila=istunto.tila,
        scoreboard=scoreboard,
        viimeisin=viimeisin,
        viesti=viesti,
        ended=bool(voittaja),
    )
    return html


@app.get("/")
def etusivu():
    session_id = request.cookies.get("kps_session")
    if not session_id:
        session_id = str(uuid4())
    tila = request.args.get("mode", "a")
    istunto = _hae_istunto(session_id, tila)
    vastaus = make_response(_renderoi(istunto))
    vastaus.set_cookie("kps_session", session_id)
    return vastaus


@app.post("/pelaa")
def pelaa():
    session_id = request.cookies.get("kps_session") or str(uuid4())
    tila = request.form.get("mode", "a")
    eka = (request.form.get("siirto1") or "").strip().lower()
    toka_syote = (request.form.get("siirto2") or "").strip().lower()

    istunto = _hae_istunto(session_id, tila)

    if istunto.tuomari.voittaja():
        vastaus = make_response(_renderoi(istunto, "Ottelu on jo päättynyt."))
        vastaus.set_cookie("kps_session", session_id)
        return vastaus

    if tila == "a":
        if eka not in _ALLOWED or toka_syote not in _ALLOWED:
            vastaus = make_response(_renderoi(istunto, "Syötä k/p/s molemmille pelaajille."))
            vastaus.set_cookie("kps_session", session_id)
            return vastaus
        toka = toka_syote
    elif tila in ("b", "c"):
        if eka not in _ALLOWED:
            vastaus = make_response(_renderoi(istunto, "Syötä k/p/s ensimmäiselle pelaajalle."))
            vastaus.set_cookie("kps_session", session_id)
            return vastaus
        toka = istunto.ai.anna_siirto()
        istunto.ai.aseta_siirto(eka)
    else:
        return redirect("/?mode=a")

    istunto.tuomari.kirjaa_siirto(eka, toka)
    tulos = _analysoi_siirrot(eka, toka)
    if tila in ("b", "c"):
        tulos += " (AI)"
    istunto.viimeisin = (eka, toka, tulos)

    vastaus = make_response(_renderoi(istunto))
    vastaus.set_cookie("kps_session", session_id)
    return vastaus


@app.post("/reset")
def resetoi():
    session_id = request.cookies.get("kps_session") or str(uuid4())
    tila = request.form.get("mode", "a")
    istunto = _hae_istunto(session_id, tila)
    istunto.nollaa(tila)

    vastaus = make_response(_renderoi(istunto, "Tulokset nollattu."))
    vastaus.set_cookie("kps_session", session_id)
    return vastaus


_TEMPLATE = """<!doctype html>
<html lang=\"fi\">
<head>
  <meta charset=\"utf-8\" />
  <title>Kivi-Paperi-Sakset</title>
  <style>
    :root { --bg: #0f172a; --card: #0b2045; --accent: #f97316; --accent2: #facc15; --text: #e2e8f0; }
    * { box-sizing: border-box; font-family: 'IBM Plex Sans', 'Segoe UI', sans-serif; }
    body { margin: 0; min-height: 100vh; background: radial-gradient(circle at 20% 20%, #123, #0f172a 40%),
                 radial-gradient(circle at 80% 30%, #0a274a, #0f172a 45%),
                 linear-gradient(135deg, #0f172a, #0b1530 60%);
           color: var(--text); display: flex; align-items: center; justify-content: center; padding: 32px; }
    .shell { width: min(900px, 95vw); background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.0));
             border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 28px; box-shadow: 0 20px 60px rgba(0,0,0,0.45); }
    h1 { margin: 0 0 16px; letter-spacing: 0.02em; font-size: 28px; }
    p.lead { margin-top: 0; color: #cbd5e1; }
    form { display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
    .card { background: var(--card); border-radius: 12px; padding: 16px 18px; border: 1px solid rgba(255,255,255,0.06); box-shadow: inset 0 1px 0 rgba(255,255,255,0.04); }
    label { display: block; margin-bottom: 6px; color: #cbd5e1; font-size: 14px; letter-spacing: 0.01em; }
    select, input { width: 100%; padding: 10px 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.15); background: rgba(255,255,255,0.04); color: var(--text); font-size: 16px; }
    .hint { font-size: 13px; color: #a5b4fc; margin-top: 4px; }
    .actions { grid-column: 1 / -1; display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
    button { background: linear-gradient(135deg, var(--accent), var(--accent2)); color: #0f172a; border: none; border-radius: 999px; padding: 12px 18px;
             font-weight: 700; cursor: pointer; transition: transform 120ms ease, box-shadow 120ms ease; }
    button:hover { transform: translateY(-1px); box-shadow: 0 10px 24px rgba(0,0,0,0.35); }
    .pill { padding: 10px 14px; border-radius: 999px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); font-size: 14px; }
    .muted { color: #cbd5e1; }
    .error { color: #fca5a5; font-weight: 600; }
  </style>
</head>
<body>
  <div class=\"shell\">
    <h1>Kivi – Paperi – Sakset</h1>
    <p class=\"lead\">Valitse pelitila ja tee siirrot. Käytössä on sama logiikka kuin komentorivipelissä.</p>

    {% if viesti %}<p class=\"error\">{{ viesti }}</p>{% endif %}

    <form method=\"post\" action=\"/pelaa\">
      <div class=\"card\">
        <label for=\"mode\">Pelitila</label>
        <select name=\"mode\" id=\"mode\" onchange=\"toggleSecond()\">
          <option value=\"a\" {% if tila == 'a' %}selected{% endif %}>Kaksinpeli (a)</option>
          <option value=\"b\" {% if tila == 'b' %}selected{% endif %}>Helppo AI (b)</option>
          <option value=\"c\" {% if tila == 'c' %}selected{% endif %}>Vaikeampi AI (c)</option>
        </select>
        <p class=\"hint\">Kivi = k, Paperi = p, Sakset = s</p>
      </div>

      <div class=\"card\">
        <label for=\"siirto1\">Ensimmäisen pelaajan siirto</label>
        <input name=\"siirto1\" id=\"siirto1\" maxlength=\"1\" autocomplete=\"off\" placeholder=\"k / p / s\" required />
      </div>

      <div class=\"card\" id=\"p2\">
        <label for=\"siirto2\">Toisen pelaajan siirto</label>
        <input name=\"siirto2\" id=\"siirto2\" maxlength=\"1\" autocomplete=\"off\" placeholder=\"k / p / s\" />
        <p class=\"hint\">Piilotetaan AI-tiloissa automaattisesti.</p>
      </div>

      <div class=\"actions\">
                <button type="submit" {% if ended %}disabled style="opacity:0.6; cursor:not-allowed;"{% endif %}>Pelaa kierros</button>
                <button type="submit" formaction="/reset" formmethod="post" style="background:rgba(255,255,255,0.08); color:var(--text);">Nollaa ottelu</button>
                <span class="pill">{{ scoreboard }}</span>
                <span class="muted">Viimeisin: {{ viimeisin }}</span>
      </div>
    </form>
  </div>

  <script>
    const mode = document.getElementById('mode');
    const p2 = document.getElementById('p2');
    function toggleSecond() {
      if (mode.value === 'a') { p2.style.display = 'block'; }
      else { p2.style.display = 'none'; document.getElementById('siirto2').value = ''; }
    }
    toggleSecond();
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True)
