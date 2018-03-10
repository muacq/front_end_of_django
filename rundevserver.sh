# modify database scheme acording to the change of models.py
python ace_new/manage.py makemigrations

#  apply database scheme change to database
python ace_new/manage.py migrate

if [ $# -ge 1 ]; then
    python ace_new/manage.py runserver 0.0.0.0:$1  # run Django development server on specify port
else
    python ace_new/manage.py runserver 0.0.0.0:8767  # run Django development server on default port 8080
fi
