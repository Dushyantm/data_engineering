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
