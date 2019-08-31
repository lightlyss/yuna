FROM python:3.7.4-alpine as production

USER root
WORKDIR /yuna
COPY . ./

RUN apk --no-cache add jpeg-dev zlib-dev make gcc g++
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-u", "yuna.py"]
