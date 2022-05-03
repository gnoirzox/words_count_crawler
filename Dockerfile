FROM python:3.10.4-slim-buster

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY /app .

EXPOSE 8000

CMD ["uvicorn", "api:app"]
