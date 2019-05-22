### Build app image

```bash
$ docker build -t bmwlog .
$ docker run -it -p 8031:8031 bmwlog
$ docker tag bmwlog:latest
$ $(aws ecr get-login --no-include-email --region us-east-1)
$ docker push 457398059321.dkr.ecr.us-east-1.amazonaws.com/whereisqa:latest
```
