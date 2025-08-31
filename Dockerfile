# 1. Base image
FROM python:3.11-slim
LABEL maintainer="medigenie"

ENV PYTHONUNBUFFERED=1 \
    PATH="/py/bin:$PATH"

# 2. System deps
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1 \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Create venv
RUN python -m venv /py && /py/bin/pip install --no-cache-dir --upgrade pip

# 4. Copy requirements first (cache layer)
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# 5. Install deps
ARG DEV=false
RUN /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt; fi && \
    rm -rf /root/.cache/pip

# 6. Copy project files after deps
COPY ./app /app
COPY ./scripts/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

WORKDIR /app
EXPOSE 8000

CMD ["sh", "-c", "/wait-for-it.sh db:5432 -- /start.sh gunicorn medigenie.wsgi:application --bind 0.0.0.0:8000"]
