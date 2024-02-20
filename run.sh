python3 manage.py makemigrations
python3 manage.py migrate
#python3 manage.py shell -c "from employee.models import Employee; Employee.objects.create_superuser('m', 'x@y.com', 'm')"
python3 manage.py runserver 0.0.0.0:8000
