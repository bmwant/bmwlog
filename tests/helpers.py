import docker
import click


def note(message):
    click.secho(message, fg='green')


def info(message):
    click.secho(message, fg='yellow')


def run_mysql_container():
    client = docker.from_env()
    container_name = 'local-mysql'
    container = client.containers.run(
        'mysql',
        name=container_name,
        auto_remove=True,
        environment={
            'MYSQL_ALLOW_EMPTY_PASSWORD': True,
        },
        detach=True,
    )
    return container


def get_container_ip_address(container):
    client = docker.from_env()
    container_data = client.api.inspect_container(container.name)
    ip_address = container_data\
        .get('NetworkSettings')\
        .get('Networks')\
        .get('bridge')\
        .get('IPAddress')
    return ip_address


def remove_container(container):
    client = docker.from_env()
    client.api.kill(container.id)

    # No need to remove. `auto_remove` flag above is provided
    # client.api.remove_container(container.id)
