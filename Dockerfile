FROM python:3
ENV PYTHONUNBUFFERED=1

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "-u", "TWDS_Crawler.py"]