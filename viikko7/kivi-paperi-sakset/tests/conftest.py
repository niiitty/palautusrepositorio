import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture(autouse=True)
def clear_sessions():
    try:
        from web_app import _ISTUNNOT
        _ISTUNNOT.clear()
    except Exception:
        pass
    yield
    try:
        from web_app import _ISTUNNOT
        _ISTUNNOT.clear()
    except Exception:
        pass


@pytest.fixture()
def client():
    from web_app import app

    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client
