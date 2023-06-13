FROM python:3.9

WORKDIR /code

COPY . .
 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "service.main:app", "--host", "0.0.0.0", "--port", "80"]

# Build the Docker image
# docker build -t your-image-name .

# Run the Docker container and mount the database file as a volume
# docker run -p 8000:8000 -v /path/to/your-database.db:/app/your-database.db your-image-name
