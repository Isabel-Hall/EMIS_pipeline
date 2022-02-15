FROM python:3.8.12-slim-bullseye

WORKDIR /app

RUN pip install fire fhir.resources dvc pymongo

RUN apt update && apt install git -y

ENTRYPOINT ["dvc", "repro"]
#ENTRYPOINT ["/bin/bash"]