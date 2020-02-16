FROM python:3.8
ADD . cooley.tech
WORKDIR cooley.tech

RUN ["pip3","install","-r","requirements.txt"]

ENTRYPOINT ["python3","-u"]
CMD ["site.py"]