FROM python:3.10-bullseye

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "health.py"]