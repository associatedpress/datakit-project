import click


def read_multichoice_or_all_input(question):
    response = click.prompt(question, type=click.STRING)
    return [val.strip() for val in response.split(' ')]
