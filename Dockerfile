FROM python:3.8
ADD . cooley.tech-sample
WORKDIR cooley.tech-sample

RUN ["pip","install","-r","requirements.txt"]

ENTRYPOINT ["python","-u"]
CMD ["site.py"]