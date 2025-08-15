FROM python:3.11-slim
LABEL maintainer="medigenie"

ENV PYTHONUNBUFFERED=1

# Install dependencies for OpenCV and other libraries
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY ./app /app
COPY ./app/core/management/commands/wait_for_db.py /app/core/management/commands/wait_for_db.py

COPY ./scripts/wait-for-it.sh /wait-for-it.sh  
RUN chmod +x /wait-for-it.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --default-timeout=100 --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi && \
    rm -rf /tmp 

ENV PATH="/py/bin:$PATH"

CMD [ "sh", "-c", "/wait-for-it.sh db:5432 -- /start.sh gunicorn medigenie.wsgi:application --bind 0.0.0.0:8000" ]
