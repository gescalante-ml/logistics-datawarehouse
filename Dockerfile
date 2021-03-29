FROM python:3.8
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt
ENV DWH_DATABASE=logistics
ENV DWH_HOST='db'
ENV DWH_USER=root
ENV DWH_PASSWORD=password

COPY . .
CMD ["python", "-u", "populate.py"]
