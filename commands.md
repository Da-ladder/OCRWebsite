Save pip versions to a .txt file
pip freeze > requirements.txt

Website to see stuff
http://0.0.0.0:8000/

Activate virtual environment
.\venv\Scripts\activate

Start docker container
docker-compose up -d --build

Go into docker shell
docker exec -it django /bin/sh

Start python file inside of shell (where celery tasks are performed)
python manage.py shell

