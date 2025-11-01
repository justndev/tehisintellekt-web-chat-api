import pytest
from unittest.mock import patch
from app.services.validation_service import ValidationService
from app.dtos.validation_response import ValidationResponse


class TestValidationService:

    @pytest.fixture
    def valid_question(self):
        return "What is the meaning of life?"

    def test_validate_question_valid(self, valid_question):
        result = ValidationService.validate_question(valid_question)

        assert isinstance(result, ValidationResponse)
        assert result.is_valid is True

    def test_validate_question_at_min_length(self):
        with patch('app.services.validation_service.MIN_QUESTION_LENGTH', 5):
            question = "Hello"
            result = ValidationService.validate_question(question)

            assert result.is_valid is True
            assert result.details == 'Question is valid'

    def test_validate_question_at_max_length(self):
        with patch('app.services.validation_service.MAX_QUESTION_LENGTH', 1000):
            question = "a" * 1000
            result = ValidationService.validate_question(question)

            assert result.is_valid is True
            assert result.details == 'Question is valid'

    def test_validate_question_empty_string(self):
        result = ValidationService.validate_question("")

        assert result.is_valid is False
        assert result.details == 'No question provided'

    def test_validate_question_whitespace_only(self):
        result = ValidationService.validate_question("   ")

        assert result.is_valid is False
        assert result.details == 'No question provided'

    def test_validate_question_tabs_and_newlines(self):
        result = ValidationService.validate_question("\t\n  \n\t")

        assert result.is_valid is False
        assert result.details == 'No question provided'

    def test_validate_question_none(self):
        result = ValidationService.validate_question(None)

        assert result.is_valid is False
        assert result.details == 'No question provided'

    def test_validate_question_too_short(self):
        with patch('app.services.validation_service.MIN_QUESTION_LENGTH', 10):
            question = "Hi?"
            result = ValidationService.validate_question(question)

            assert result.is_valid is False
            assert result.details

    def test_validate_question_too_long(self):
        with patch('app.services.validation_service.MAX_QUESTION_LENGTH', 1000):
            question = "a" * 1001
            result = ValidationService.validate_question(question)

            assert result.is_valid is False
            assert result.details == 'Question is too long. Maximum length is 1000 characters'

