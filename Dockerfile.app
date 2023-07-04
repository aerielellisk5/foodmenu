FROM python:latest

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 3000

ENTRYPOINT [ "python3" ]

CMD ["-u", "app.py"]

# docker build docker build --no-cache -t foodmenu_app:v4 -f Dockerfile.app .
# docker run -dp 3000:3000 --name foodmenu_app_container1 --network foodmenu_app:v1 