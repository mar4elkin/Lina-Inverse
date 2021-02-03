FROM python:3.8-alpine
WORKDIR /app/backend
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "main.py"]