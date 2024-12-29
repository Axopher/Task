# SIMPLE DJANGO PROJECT MANAGEMENT DEMO APP

## If you are using Docker:

1. Open the .env file on a text editor and uncomment the line DATABASE_URL=postgres://postgres:password@db:5432/postgres
2. Open a new command line window and go to the project's directory
3. Run the setup: make docker_setup
4. Access http://localhost:8000/swagger/ on your browser


Other Commands:
- To access the logs for individual service, run: make docker_logs <service name> (either backend or db)
- To stop the project, run: make docker_down
- To create the migrations for app: make docker_makemigrations
- To run the migrations: make docker_migrate
- To run the project: make docker_up

## If you are not using Docker:
1. Open the .env file on a text editor and do one of the following:
    - If you wish to use SQLite locally, uncomment the line DATABASE_URL=sqlite:///db.sqlite3
    - If you wish to use PostgreSQL locally, uncomment and edit the line DATABASE_URL=postgres://postgres:postgres@postgres:5432/postgres 
    - In order to make it correctly point to your database URL. The url format is the following: postgres://USER:PASSWORD@HOST:PORT/NAME

2. After that open a command line window and go to the project's directory

1. Run
```
python3 -m venv venv
``` 
2. Run
```
source venv/bin/activate
```
3. RUN
```
pip install -r requirements.txt
```
4. RUN
```
python manage.py runserver
```
5. RUN
```
python manage.py makemigrations
```
6. RUN
```
python manage.py migrate
```
7. Go to http://localhost:8000/swagger/

----

## Additionally

### To import Postman collection,

1. click on import tab of postman and enter this url: `http://localhost:8000/swagger/?format=openapi`
2. You may also want to explore from admin side for which RUN on  command line window
```
python manage.py createsuperuser
```
and explore http://localhost:8000/admin/