import string

import pytest

from password_generator import generate_password


class TestGeneratePassword:
    def test_default_length_is_16(self):
        assert len(generate_password()) == 16

    @pytest.mark.parametrize("length", [8, 12, 20, 32])
    def test_respects_requested_length(self, length):
        assert len(generate_password(length=length)) == length

    def test_raises_when_no_character_types_selected(self):
        with pytest.raises(ValueError):
            generate_password(
                use_upper=False, use_lower=False, use_digits=False, use_special=False
            )

    def test_uses_only_selected_character_types(self):
        password = generate_password(
            length=32, use_upper=True, use_lower=False, use_digits=False, use_special=False
        )
        assert all(c in string.ascii_uppercase for c in password)

    def test_guarantees_at_least_one_of_each_selected_type(self):
        for _ in range(50):
            password = generate_password(length=8)
            assert any(c in string.ascii_uppercase for c in password)
            assert any(c in string.ascii_lowercase for c in password)
            assert any(c in string.digits for c in password)
            assert any(c in "!@#$%^&*()" for c in password)

    def test_single_category_password_still_guarantees_one_character(self):
        password = generate_password(
            length=8, use_upper=False, use_lower=False, use_digits=True, use_special=False
        )
        assert len(password) == 8
        assert all(c in string.digits for c in password)

    def test_passwords_are_not_deterministic(self):
        passwords = {generate_password() for _ in range(10)}
        assert len(passwords) > 1
