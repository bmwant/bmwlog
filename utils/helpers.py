import click


def note(message):
    click.secho(message, fg='green')


def info(message):
    click.secho(message, fg='yellow')


def warn(message):
    click.secho(message, fg='red')
