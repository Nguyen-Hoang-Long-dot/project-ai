import importlib
import sys
from unittest.mock import patch


def test_main_does_not_seed_on_import():
    sys.modules.pop("main", None)

    with patch("app.db.seed.seed_data") as mock_seed:
        importlib.import_module("main")

    mock_seed.assert_not_called()
