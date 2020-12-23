FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app

COPY ./requirements.txt app/requirements.txt

COPY ./punkt.py app/punkt.py

RUN pip install -r app/requirements.txt

RUN python app/punkt.py