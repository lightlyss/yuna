FROM tensorflow/tensorflow:1.13.2 as production

USER root
WORKDIR /yuna
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt
CMD ["flask", "run", "--host=0.0.0.0"]
