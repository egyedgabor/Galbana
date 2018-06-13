# Galbana (Elasticsearch reporting tool)

Docker based setup for a simple Django-Postgres-Nginx

## Set Environmental Variable

* Set the .env file (root:root 600) based on .env_sample
* Set ssh .secrets
  * nginx
    * certificate.key (4430:4430 600)
    * certififcate.crt (4430:4430 644)
    * ca.crt (4430:4430 644)
  * django (need certificate to connect elasticsearch)
    * certificate.pem (8000:8000 600) (cat certificate.key certififcate.crt)
    * certificate.key (8000:8000 600)
    * certififcate.crt (8000:8000 644)
    * ca.crt (8000:8000 644)
    * DB_PASSWORD (8000:8000 600)
    * DJANGO_SECRET_KEY (8000:8000 600)
  * postgres
    * DB_PASSWORD (999:999 600)

## Set Production files

* Copy makefile from the git repository
* Copy docker-compose.yml

## Update

* On dev:

```sh
make push
```

## On prod:

* set the new IMAGE_TAG in the .env file

```sh
docker-compose down
docker-compose up
```
