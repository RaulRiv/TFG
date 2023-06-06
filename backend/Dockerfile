FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .
ENV DATABASE_URL=./database/sql_app.db

CMD ["uvicorn", "service.main:app", "--host", "0.0.0.0", "--port", "80"]