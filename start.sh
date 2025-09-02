echo "Running migrations ....."
python3 manage.py migrate --noinput 

echo "Checking if cities data already exists ...."
python3 manage.py shell <<EOF
from cities_light.models import City
if not City.objects.exists():
    from django.core.management import call_command
    print("No cities found. Loading cities data...")
    call_command("cities_light")
else:
    print("Cities already loaded. Skipping cities_light command.")
EOF

echo "Collecting static files ...."
python3 manage.py collectstatic --noinput

echo "Creating default superuser if not already exist ...."
python3 manage.py shell <<EOF

from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="admin@example.com").exists():
    User.objects.create_superuser(email="admin@example.com", password="admin", role="Admin")

EOF

echo "Starting the server ...."
exec "$@"