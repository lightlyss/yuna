FROM python:3.5.7-slim
USER root
WORKDIR /yuna

RUN apt-get update -q
RUN apt-get install --no-install-recommends -qy make gcc g++

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY cache/ ./cache/
COPY *.py ./

CMD ["python", "-u", "yuna.py"]
