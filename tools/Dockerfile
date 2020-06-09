FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
COPY ./ /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:8080"]
