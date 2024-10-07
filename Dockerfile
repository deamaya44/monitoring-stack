FROM python:3.9-slim

WORKDIR /app

COPY dispatcher.py /app/dispatcher.py

RUN pip install Flask requests

EXPOSE 5000

CMD ["python", "dispatcher.py"]
