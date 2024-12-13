## Setup PostgreSQL Database

To set up a PostgreSQL database, run the following command:

```bash
docker run -it \
  -e POSTGRES_USER="dushyant" \
  -e POSTGRES_PASSWORD="dushyant" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_db:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

## Connect to PostgreSQL Database

To connect to the PostgreSQL database, use `pgcli`:

```bash
pgcli -h localhost -p 5432 -u dushyant -d ny_taxi
```

## Dataset

Download the dataset using the following command:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

## Data Dictionary

Refer to the [data dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf) for more information about the dataset.


## PGAdmin for database management and visualization

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="dushyant" \
  -p 8080:80 \
  dpage/pgadmin4
```

## create docker network to run the containers

```bash
docker network create pg_network
```

## run the containers in the network

```bash
docker run -it \
  -e POSTGRES_USER="dushyant" \
  -e POSTGRES_PASSWORD="dushyant" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_db:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg_network \
  --name pg_database \
  postgres:13
```

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="dushyant" \
  -p 8080:80 \
  --network=pg_network \
  --name pg_admin \
  dpage/pgadmin4
```

## Injest data using python script

```bash
python injest_dataset.py --user=dushyant --host=localhost --port=5432 --db=ny_taxi --table_name=yellow_taxi_trips --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
```

## Build the docker image
docker build -t taxi_injest:v01 .

## Run the docker image
docker run -it \
  --network=pg_network \
  taxi_injest:v01 \
  --user=dushyant \
  --host=pg_database \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

## Run the docker compose
docker compose up -d