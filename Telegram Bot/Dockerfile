FROM arm64v8/python:3.7.10-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "./main.py", "-t", "True", "-d", "True"]
