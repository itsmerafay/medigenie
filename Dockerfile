FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Required OS dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy source code
COPY ./app /app
COPY ./app/core/management/commands/wait_for_db.py /app/core/management/commands/wait_for_db.py
COPY ./scripts/wait-for-it.sh /wait-for-it.sh
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN chmod +x /wait-for-it.sh

WORKDIR /app

# Setup virtual env
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    /py/bin/pip install -r /tmp/requirements.dev.txt

ENV PATH="/py/bin:$PATH"

EXPOSE 8000

CMD [ "sh", "-c", "/wait-for-it.sh db:5432 -- python manage.py wait_for_db && python manage.py migrate && gunicorn medigenie.wsgi:application --bind 0.0.0.0:8000" ]
