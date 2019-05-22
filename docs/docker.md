### Build app image

```bash
$ docker build -t bmwlog .
$ docker run -it -p 8031:8031 --env-file=.dev.env bmwlog
$ docker tag bmwlog:latest bmwant/bmwlog:latest
$ docker push bmwant/bmwlog:latest
```


### Launch application locally with Docker Compose

```bash
$ docker-compose up
```
