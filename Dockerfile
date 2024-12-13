FROM python:3.9.1

RUN pip install pandas sqlalchemy python-dotenv psycopg2-binary wget

WORKDIR /app

COPY injest_dataset.py injest_dataset.py

COPY .env .env

ENTRYPOINT [ "python" , "injest_dataset.py" ]