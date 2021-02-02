FROM python:3.8-alpine
WORKDIR /app/frontend
COPY . .
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN pip install -r requirements.txt
CMD ["python", "main.py"]

