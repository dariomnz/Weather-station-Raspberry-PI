FROM python:3.7.3

COPY /app /etc/usr/src/app

WORKDIR /etc/usr/src/app

# Install any needed packages
RUN pip install mysql-connector-python Flask Flask-Cors PyYAML

# Run python script when the container launches
ENTRYPOINT ["python"]
CMD ["-u","measurements_manager_api.py"]