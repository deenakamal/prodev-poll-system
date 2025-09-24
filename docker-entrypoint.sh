#!/bin/bash
set -e

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Load fixtures if no Poll exists
count=$(python manage.py shell --quiet -c "from polls.models import Poll; print(Poll.objects.count())")
if [ "$count" -eq 0 ]; then
    python manage.py loaddata initial_data.json
fi

# Run server
python manage.py runserver 0.0.0.0:8000
