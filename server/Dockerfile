FROM tensorflow/tensorflow:1.15.0-py3
USER root
WORKDIR /yuna

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY afdmodel/ ./afdmodel/
COPY Makefile ./
RUN make defrag-model

ENV FLASK_APP="yuna.py"
COPY static/ ./static/
COPY afd/ ./afd/
COPY *.py ./

EXPOSE 5000/tcp
CMD ["flask", "run", "--host=0.0.0.0"]
