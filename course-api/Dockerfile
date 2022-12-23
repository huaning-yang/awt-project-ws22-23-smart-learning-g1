# https://hub.docker.com/r/library/python/tags/
FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copying source in current directory into the image
COPY . /usr/src/app

# Commands in a list

#RUN chmod a+x /usr/src/app/run.sh
#CMD ["/usr/src/app/run.sh"]
CMD ["python", "/usr/src/app/api.py"]