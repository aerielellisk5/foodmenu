FROM python:latest

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 3000

ENTRYPOINT [ "python3" ]

CMD ["app.py"]