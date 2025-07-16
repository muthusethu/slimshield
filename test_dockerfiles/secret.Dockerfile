# test_dockerfiles/secret.Dockerfile
FROM python:3.10

ENV SECRET_KEY="super-secret-token"
RUN echo "password=123456" >> /app/config.txt
