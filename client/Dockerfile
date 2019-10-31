FROM python:3.6.9-slim
USER root
WORKDIR /yuna

RUN apt-get update -q
RUN apt-get install --no-install-recommends -qy make

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV YUNA_HOST="http://yuna:5000"
COPY cache/ ./cache/
COPY Makefile ./
COPY *.py ./

CMD ["python", "-u", "yuna.py"]
