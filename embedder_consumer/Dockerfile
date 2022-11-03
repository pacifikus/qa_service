FROM tensorflow/tensorflow:latest

RUN apt-get update && \
    apt-get install -y python3.7 python3-pip python3-setuptools python3-distutils
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir /.cache
RUN chown -R 1100:1100 /.cache

ENTRYPOINT ["python", "consumer.py"]
