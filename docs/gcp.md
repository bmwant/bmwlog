### Create MySQL database

Activate target project first

```bash
$ gcloud projects list
$ gcloud config set project bmwlog
$ gcloud config get-value project
```

Create CloudSQL instance

```bash
$ gcloud sql instances create bmwlogdb --tier=db-f1-micro --region=us-east1
```

Create a database on the instance

```bash
$ gcloud sql databases create bmwlogdb --instance=bmwlogdb \
    --charset=utf8 --collation=utf8_general_ci
```

Configure default user

```bash
$ gcloud sql users set-password root \
    --host=% --instance=bmwlogdb --prompt-for-password
```

List databases available

```bash
$ gcloud sql databases list --instance=bmwlogdb
```

### Connect to the database

```bash
$ ./cloud_sql_proxy -instances=bmwlog:us-east1:bmwlogdb=tcp:3306
$ mysql -u root -p --host 127.0.0.1
```

Restore database from a dump

```bash
$ mysql -u root -p --host 127.0.0.1 bmwlogdb < dump.sql
```
