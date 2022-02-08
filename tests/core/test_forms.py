import pytest
from django.forms.widgets import PasswordInput

from core.forms import SettingsForm


@pytest.mark.django_db
def test_valid_settings_form():
    form = SettingsForm(
        data={
            "remote_system_base_url": "https://example.com",
            "aws_access_key_id": "123456789",
            "aws_secret_access_key": "0987654321",
            "aws_bucket_name": "bucket-bucket",
        }
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_invalid_settings_form_missing_data():
    form = SettingsForm(
        data={
            "remote_system_base_url": "https://example.com",
            "aws_secret_access_key": "0987654321",
            "aws_bucket_name": "bucket-bucket",
        }
    )
    print(form.errors)
    assert not form.is_valid()


@pytest.mark.django_db
def test_invalid_settings_form_bad_URL():
    form = SettingsForm(
        data={
            "remote_system_base_url": "$2389f",
            "aws_access_key_id": "123456789",
            "aws_secret_access_key": "0987654321",
            "aws_bucket_name": "bucket-bucket",
        }
    )
    assert not form.is_valid()


@pytest.mark.django_db
def test_invalid_settings_form_too_long_charfield():
    form = SettingsForm(
        data={
            "remote_system_base_url": "www.example.com",
            "aws_access_key_id": """9EXmwWxxXLskbdSXYsvqkPHl1FNEHMwWPtJWd8geZeZQwD1Tvb98OitYMMMoO4gVYmm5WMBgy5vTXjC7oO0B
                                e8MQ7JkbMe6B07P39vZIyJQgHr3uQxcZt3wzcP5cuj09QNkS0u2mTNAvq2kg1LtfN5RA0xnWuzssb5xgTbIsiE9t
                                NWwpmlBekCGzUhxmIMVjjn3sIXl5fLn0oxq7LMBQMniKnaiwWKqCUmhtcUkYm6kDlAdxJOB1DAqs9qAZbHskBsm
                                nMbzghSnDcPRxSy5fpTd85Ruj5Dw5SOVwmnSdrkzXiS2tw8Q2KS2aDa76iVh9aihc5T8n1XfwUOF0X1Sthwreb5b
                                A0iarJ4Q6WnKfdrYRZhEh2dfvjHOuxQ2as6uV11A0SrEylaVMUUVx""",
            "aws_secret_access_key": "0987654321",
            "aws_bucket_name": "bucket-bucket",
        }
    )
    assert not form.is_valid()


@pytest.mark.django_db
def test_access_key_widget_overrides_correctly():
    form = SettingsForm()
    assert type(form.fields["aws_access_key_id"].widget) == PasswordInput


@pytest.mark.django_db
def test_secret_key_widget_overrides_correctly():
    form = SettingsForm()
    assert type(form.fields["aws_secret_access_key"].widget) == PasswordInput
