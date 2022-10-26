FROM python:3.10.5

WORKDIR /e-recycle-core 

COPY . . 

EXPOSE 8000 

ENTRYPOINT ["tail", "-f", "/dev/null"]