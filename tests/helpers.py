import docker


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

    ip_address = client.api.inspect_container(container_name)['NetworkSettings']['Networks']['bridge']['IPAddress']
    return ip_address


# docker.pull('redis')
# port = unused_port()
# container = docker.create_container(
#     image='redis',
#     name='test-redis-{}'.format(session_id),
#     ports=[6379],
#     detach=True,
#     host_config=docker.create_host_config(
#         port_bindings={6379: port}))
# docker.start(container=container['Id'])
# yield port
# docker.kill(container=container['Id'])
# docker.remove_container(container['Id'])

