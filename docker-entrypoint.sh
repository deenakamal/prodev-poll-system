#!/bin/bash
set -e

# Apply migrations
python manage.py makemigrations
python manage.py migrate


# Load fixtures if no Poll exists
count=$(python -c "import django, os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','poll_backend.settings'); django.setup(); from polls.models import Poll; print(Poll.objects.count())" | xargs)

if [ $count -eq 0 ]; then
    echo "No Polls found → loading initial fixtures..."
    python manage.py loaddata polls/fixtures/initial_data.json
fi

# Run server
python manage.py runserver 0.0.0.0:8000
