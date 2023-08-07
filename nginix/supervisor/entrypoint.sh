#!/bin/bash
set -e

# Start supervisord in the background
supervisord -c /etc/supervisor/conf.d/supervisord.conf &

# Add any additional startup commands here, if needed

# Run the CMD instructions passed by Docker at container startup
exec "$@"
