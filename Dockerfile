FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /databox-service
WORKDIR /databox-service
COPY ./requirements.txt /databox-service/requirements.txt
RUN git clone https://github.com/databox/databox-python.git /databox-service/databox-python
WORKDIR /databox-service/databox-python/src
RUN pip3 install .
WORKDIR /databox-service
RUN pip3 install -r requirements.txt
COPY ./local_data/* /databox-service/
ENV PYTHONPATH $PYTHONPATH:/workdir
#CMD ["python3", "main.py"]


# for tests run
CMD ["sh", "-c", "coverage run test_runner.py && coverage report -m && coverage html -d /databox-service/coverage_report"]
