import requests

from password_checker import check_password, check_hibp, get_strength
from password_strength import PasswordStrength


class TestCheckPassword:
    def test_valid_password_returns_none(self):
        assert check_password("Abcdefg1!") is None

    def test_too_short(self):
        assert "at least 8 characters" in check_password("Ab1!")

    def test_missing_uppercase(self):
        assert "uppercase" in check_password("abcdefg1!")

    def test_missing_lowercase(self):
        assert "lowercase" in check_password("ABCDEFG1!")

    def test_missing_digit(self):
        assert "digit" in check_password("Abcdefgh!")

    def test_missing_special_character(self):
        assert "special character" in check_password("Abcdefgh1")

    def test_checks_are_ordered_length_first(self):
        # A short password missing everything else should still report length first.
        assert "at least 8 characters" in check_password("a")

    def test_complex_password_is_accepted(self):
        assert check_password("Kj9!TpZmQr") is None


class TestGetStrength:
    def test_empty_password_is_weak(self):
        assert get_strength("") == PasswordStrength.WEAK

    def test_short_simple_password_is_weak(self):
        assert get_strength("abcdefg") == PasswordStrength.WEAK

    def test_moderate_password_is_fair(self):
        assert get_strength("Kjqmzvbt") == PasswordStrength.FAIR

    def test_long_varied_password_is_strong_or_better(self):
        strength = get_strength("Kj9!TpZmQr")
        assert strength in (PasswordStrength.STRONG, PasswordStrength.VERY_STRONG)

    def test_long_fully_varied_password_is_very_strong(self):
        assert get_strength("Kj9!TpZmQr7XvBn2") == PasswordStrength.VERY_STRONG

    def test_repeated_character_run_lowers_score(self):
        # Same character variety as "Kjqmzvbt" (upper+lower, no digit/special),
        # but "AAAA" is a low-entropy repeated run that should drag it down.
        varied = get_strength("Kjqmzvbt")
        repeated = get_strength("AAAAaaaa")
        assert varied == PasswordStrength.FAIR
        assert repeated == PasswordStrength.WEAK

    def test_sequential_run_lowers_score(self):
        # "abcd" is a classic low-entropy sequential pattern.
        assert get_strength("abcd1234") == PasswordStrength.WEAK


class FakeResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"status {self.status_code}")


class TestCheckHibp:
    def test_pwned_password_returns_true_with_count(self, monkeypatch):
        # SHA-1 of "password" is 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
        def fake_get(url, timeout):
            assert url.endswith("/range/5BAA6")
            return FakeResponse("1E4C9B93F3F0682250B6CF8331B7EE68FD8:12345\nOTHERSUFFIX:1")

        monkeypatch.setattr(requests, "get", fake_get)

        pwned, count = check_hibp("password")
        assert pwned is True
        assert count == 12345

    def test_unpwned_password_returns_false(self, monkeypatch):
        def fake_get(url, timeout):
            return FakeResponse("SOMEOTHERSUFFIX:99")

        monkeypatch.setattr(requests, "get", fake_get)

        pwned, count = check_hibp("a-very-unique-password")
        assert pwned is False
        assert count == 0

    def test_network_failure_raises(self, monkeypatch):
        def fake_get(url, timeout):
            raise requests.RequestException("network down")

        monkeypatch.setattr(requests, "get", fake_get)

        try:
            check_hibp("password")
            assert False, "expected RequestException"
        except requests.RequestException:
            pass

    def test_only_prefix_of_hash_is_sent(self, monkeypatch):
        captured = {}

        def fake_get(url, timeout):
            captured["url"] = url
            return FakeResponse("")

        monkeypatch.setattr(requests, "get", fake_get)

        check_hibp("password")
        # Only the first 5 hex characters of the SHA-1 hash should appear in the URL.
        assert captured["url"].endswith("5BAA6")
