[![Server Build](https://github.com/lightlyss/yuna/workflows/server/badge.svg)](https://github.com/lightlyss/yuna)
[![Client Build](https://github.com/lightlyss/yuna/workflows/client/badge.svg)](https://github.com/lightlyss/yuna)
# Yuna
![banner](banner.png)
> AI mascot and idol of Ordinal Scale

## Description
A Flask server that performs facial detection using deep learning, powered by
TensorFlow. Comes packaged with a Discord bot.

![demo](demo.png)

## Development
Specify `YUNA_TOKEN` inside a `.env` file or as a plain environment variable for
the Discord bot. The system is provided as a ready-to-use docker network.
`docker-compose up -d` to start. The server component will be available at port `5000`.
Running natively is presently untested, but to do so requires Python 3 and TensorFlow
in addition to Python modules listed in `requirements.txt` manifests. Relevant models
must also be recompiled manually before the server can function natively:
```bash
cd server
make defrag-model
```
