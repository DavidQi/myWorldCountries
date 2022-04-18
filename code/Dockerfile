FROM ubuntu:21.10
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y python3-pip
RUN mkdir -p /pycode
WORKDIR /pycode
COPY . /pycode
RUN cd /pycode && pip3 install -r requirements.txt
ENV PYTHONUNBUFFERED=1

#CMD [ "python3", "country_api.py"]
ENTRYPOINT ["python3", "country_code.py"]
