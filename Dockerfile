from python:latest
workdir /opt/star-burger
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD gunicorn star_burger.wsgi:application --bind 0.0.0.0:8000
