### Build app image

```bash
$ docker build -t bmwlog .
$ docker run -it -p 8031:8031 --env-file=.dev.env bmwlog
$ docker tag bmwlog:latest bmwant/bmwlog:latest
$ docker push bmwant/bmwlog:latest
```

### Create a database

[MariaDB](https://docs.docker.com/samples/library/mariadb/) images is used for the database.

Create all the system files needed for the db to run

```bash
$ docker run -it -v /usr/local/var/mariadb:/var/lib/mysql mariadb bash
$ mysql_install_db --user=mysql
$ mysqld_safe &
$ /usr/bin/mysql_secure_installation
```

### Restore database from a dump

```bash
$ docker run -it -v /usr/local/var/mariadb:/var/lib/mysql \
    -v /Users/bmwant/pr/testproject/dump.sql:/tmp/dump.sql \
    mariadb bash
$ mysqld_safe &
$ mysql -u root -p bmwlogdb < /tmp/dump.sql
```

### Launch application locally with Docker Compose

```bash
$ docker-compose up
```
