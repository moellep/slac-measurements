import functools
import sys
from types import ModuleType
from unittest.mock import MagicMock

_meme = ModuleType("meme")
_meme_model = ModuleType("meme.model")
_meme_model.Model = MagicMock()
_meme.model = _meme_model


def mock_meme(test_func):
    """Decorator: registers a fake meme/meme.model module before the test
    runs, so a @patch("meme.model.Model") stacked below this can resolve
    it -- meme is an optional dependency not installed in CI, and the code
    under test does a lazy `from meme.model import Model` inside the
    function body, so patch() needs a real module already in sys.modules
    to attach to. Must be the outer decorator (applied above @patch) so its
    wrapper runs -- and registers the module -- before @patch's own wrapper
    tries to resolve "meme.model.Model"."""

    @functools.wraps(test_func)
    def wrapper(*args, **kwargs):
        sys.modules.setdefault("meme", _meme)
        sys.modules.setdefault("meme.model", _meme_model)
        return test_func(*args, **kwargs)

    return wrapper
