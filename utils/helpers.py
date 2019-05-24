import click


def note(message):
    click.secho(f'\n==> {message}', fg='green')


def info(message):
    click.secho(f'\n==> {message}', fg='yellow')


def warn(message):
    click.secho(f'\n==> {message}', fg='red')
