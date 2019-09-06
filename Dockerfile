FROM lozuwa/python:django_k8s
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /opt/kontroller
WORKDIR ${APP_HOME} 
COPY app/ ${APP_HOME}
#ENTRYPOINT ["gunicorn"]
#CMD ["--log-level", "debug", "--config", "/opt/kontroller/gunicorn.py", "kontroller.wsgi:application"]
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]

