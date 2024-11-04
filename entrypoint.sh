#!/bin/bash

# Create a non-root user with the specified user and group IDs
if ! id -u "$UID" &>/dev/null; then
    groupadd -g "$GID" myuser
    useradd -m -u "$UID" -g "$GID" myuser
fi

# Run the script once at startup
gosu myuser python3 /coming-soon/app.py

# Write out the cron job to a temporary file
echo "SHELL=/bin/bash" > /etc/cron.d/my_cronjob
echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" >> /etc/cron.d/my_cronjob
env >> /etc/environment
echo "${CRON_SCHEDULE} gosu myuser /usr/local/bin/python3 /coming-soon/app.py >> /var/log/cron.log 2>&1" >> /etc/cron.d/my_cronjob

# Set file permissions and load the cron job
chmod 0644 /etc/cron.d/my_cronjob
crontab /etc/cron.d/my_cronjob

# Start cron in the foreground
cron -f
