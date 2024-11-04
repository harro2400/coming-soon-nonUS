FROM python:3-slim

RUN apt-get update && \
    apt-get install -y cron gosu && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install --no-cache-dir icalendar requests

COPY app-docker.py /coming-soon/app.py
COPY arial.ttf /coming-soon/arial.ttf
COPY entrypoint.sh /coming-soon/entrypoint.sh
COPY ffmpeg /coming-soon/ffmpeg

ENV CRON_SCHEDULE="0 4 * * *"
ENV UID=1000
ENV GID=1000

RUN chmod +x /coming-soon/entrypoint.sh /coming-soon/ffmpeg

CMD ["/coming-soon/entrypoint.sh"]