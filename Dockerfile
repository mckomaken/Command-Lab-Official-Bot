FROM python:3.13-alpine

WORKDIR /app

RUN apk update
RUN apk add bash git curl

# install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy sources
COPY assets /app/
COPY cogs /app/
COPY config /app/
COPY data /app/
COPY schemas /app/
COPY utils /app/
COPY CommandLab.py /app/

# create tmp directory
RUN mkdir .tmp

CMD ["python3", "/app/CommandLab.py"]