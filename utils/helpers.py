import click


def note(message):
    click.secho(message, fg='green')


def info(message):
    click.secho(message, fg='yellow')
