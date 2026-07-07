import click
import pytest

from datakit_project.prompt import read_multichoice_or_all_input


@pytest.mark.parametrize('response, expected', [
    ('all', ['all']),
    ('1 2 3', ['1', '2', '3']),
])
def test_splits_space_separated_response(monkeypatch, response, expected):
    monkeypatch.setattr(click, 'prompt', lambda question, type: response)
    assert read_multichoice_or_all_input('Pick some') == expected
