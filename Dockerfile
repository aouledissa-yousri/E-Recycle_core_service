FROM python:3.10.7 

WORKDIR /e-recycle-core 

RUN pip3 install --upgrade pip

COPY . . 

ENV PORT=8000

EXPOSE 8000

CMD ["python", "manage.py", "runserver" ]