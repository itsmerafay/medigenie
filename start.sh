echo "Running migrations ....."
python3 manage.py migrate --noinput 

echo "Collecting static files ...."
python3 manage.py collectstatic --noinput

echo "Creating default superuser if not already exist ...."
python3 manage.py shell <<EOF

from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="admin@example.com").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin")

EOF

echo "Starting the server ...."
exec "$@"