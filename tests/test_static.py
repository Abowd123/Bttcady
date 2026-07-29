import ast
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PYTHON_FILES = [
    path for path in ROOT.rglob("*.py")
    if ".git" not in path.parts
    and "backups" not in path.parts
    and "tests" not in path.parts
]


class StaticSafetyTests(unittest.TestCase):
    def test_all_python_files_parse(self):
        for path in PYTHON_FILES:
            with self.subTest(path=path.relative_to(ROOT)):
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_no_exposed_legacy_credentials(self):
        forbidden = (
            "6168217372", "5117901887", "7284348194",
            "7201745912",
            "BACPaOQ", "8a807fba", "34366457", "session_string=",
        )
        source = "\n".join(path.read_text(encoding="utf-8") for path in PYTHON_FILES)
        for value in forbidden:
            self.assertNotIn(value, source)

    def test_no_remote_execution_handlers(self):
        forbidden = (
            'filters.command("eval")', 'filters.command("cmd")',
            'filters.command("exec")', 'filters.command("print")',
            "async def aexec", "create_subprocess_shell", "os.system(",
        )
        source = "\n".join(path.read_text(encoding="utf-8") for path in PYTHON_FILES)
        for value in forbidden:
            self.assertNotIn(value, source)

    def test_no_braced_http_urls(self):
        for path in PYTHON_FILES:
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn("{https://", source)
                self.assertNotIn("{http://", source)

    def test_required_environment_configuration(self):
        config = (ROOT / "config.py").read_text(encoding="utf-8")
        for name in ("BOT_TOKEN", "API_ID", "API_HASH", "OWNER_ID"):
            self.assertIn(name, config)

    def test_no_manual_per_message_threads(self):
        source = "\n".join(path.read_text(encoding="utf-8") for path in PYTHON_FILES)
        self.assertNotIn("Thread(target=", source)

    def test_rank_handlers_have_early_routes(self):
        for relative in (
            "Plugins/set_ranks.py",
            "Plugins/get_ranks.py",
            "Plugins/del_ranks.py",
        ):
            source = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("normalize_message_text(m)", source)
            self.assertIn("matches_command(", source)

    def test_workers_are_bounded(self):
        main = (ROOT / "main.py").read_text(encoding="utf-8")
        config = (ROOT / "config.py").read_text(encoding="utf-8")
        self.assertIn("workers=config.BOT_WORKERS", main)
        self.assertIn("BOT_WORKERS", config)


if __name__ == "__main__":
    unittest.main()
