FROM python:3.7.4-alpine
USER root
WORKDIR /yuna

RUN apk --no-cache add make gcc g++
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY cache/ ./cache/
COPY *.py ./

CMD ["python", "-u", "yuna.py"]
