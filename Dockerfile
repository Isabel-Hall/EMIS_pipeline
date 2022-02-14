FROM python:3.8.12-slim-bullseye

WORKDIR /app

RUN pip install fire fhir.resources dvc 

ENTRYPOINT ["dvc", "repro"]