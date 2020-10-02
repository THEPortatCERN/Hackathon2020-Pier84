#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Run django tests
python manage.py test
if [ $? -ne 0 ]
then
  return 1
fi

# Run migrations and staticfiles
python manage.py migrate
python manage.py collectstatic --noinput
chmod -R 755 /root/humanitarian_feedback/staticfiles

exec "$@"
