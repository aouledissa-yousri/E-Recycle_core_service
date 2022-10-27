FROM python:3.10.7

WORKDIR /e-recycle-core 

COPY . . 

RUN pip install -r requirements.txt

EXPOSE 8000 

ENTRYPOINT ["python", "manage.py", "runserver"]