FROM python:3.6-alpine

COPY requirements.txt getweather.py /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "getweather.py"]
