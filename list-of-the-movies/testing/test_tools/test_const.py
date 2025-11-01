from tools.const import UNSAFE_METHODS


class TestConstants:

    def test_unsafe_methods(self) -> None:
        safe_methods = {
            "GET",
            "HEAD",
            "OPTIONS",
        }
        assert not UNSAFE_METHODS & safe_methods

    def test_all_methods_are_upper(self) -> None:
        assert all(method.isupper() for method in UNSAFE_METHODS)
