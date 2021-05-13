FROM python:3.8.3

WORKDIR /usr/src/app

COPY datasets/BTCUSDT-1H.csv .
COPY config.py .
COPY indicators.py .
COPY utils.py .
COPY model.py .
COPY multiprocessing_env.py .
COPY rlbot.py .

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "./rlbot.py"]