FROM python:3.11.5-slim

ENV PYTHONUNBUFFERED=1

# name for dockerfile
WORKDIR /app 

# some stuff
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    gcc \
    libpq-dev \
    v4l-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# list the require database
COPY requirements.txt /app/

# Copy and install the database
RUN pip install -r /app/requirements.txt

# copy all the data relate to this current files -> go for check on docker container
COPY . /app/

# port that you want to use
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
