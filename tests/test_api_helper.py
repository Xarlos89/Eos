import asyncio
import sys
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOT_SRC = ROOT / "src" / "bot"
sys.path.insert(0, str(BOT_SRC))

sys.modules.setdefault(
    "aiohttp",
    types.SimpleNamespace(ClientSession=None, ClientTimeout=lambda total: total),
)
sys.modules.setdefault("requests", types.SimpleNamespace())

from core import api_helper  # noqa: E402


class FakeResponse:
    def __init__(self, url):
        self.url = url

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        return False

    async def json(self):
        return {"url": self.url}


class FakeSession:
    calls = []

    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.get("timeout")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        return False

    def get(self, url):
        self.calls.append(url)
        return FakeResponse(url)


class HealthCheckTests(unittest.TestCase):
    def test_health_check_calls_api_and_database_endpoints(self):
        FakeSession.calls = []
        api_helper.aiohttp.ClientSession = FakeSession
        api_helper.aiohttp.ClientTimeout = lambda total: total

        api = api_helper.API()
        api.api = "http://eos.test"

        results = asyncio.run(api.health_check())

        self.assertEqual(
            FakeSession.calls,
            ["http://eos.test/hc_api", "http://eos.test/hc_db"],
        )
        self.assertEqual(results["api_status"], {"url": "http://eos.test/hc_api"})
        self.assertEqual(results["db_status"], {"url": "http://eos.test/hc_db"})


if __name__ == "__main__":
    unittest.main()
