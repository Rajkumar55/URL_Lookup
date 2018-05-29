# URL_Lookup
This service is developed using Python 3.6.5 and Django 2.0.5.
It is developed with Django Rest Framework following MVC Pattern. The DataBase used is MySQL.

## Prerequisites
The requirements.txt file contains all the necessary packages that is needed for this application. The packages can be installed using the following command:
```
pip install -r requirements.txt
```
Install MySQL and create a DataBase named 'url_lookup'

## Deployment on Local Machine
Once all the packages are installed, run the following commands sequentially:
```
python manage.py makemigrations
```
This command creates migration files from the models in Django ORM which are defined in /url_lookup/models.py

```
python manage.py migrate
```
This command creates the necessary tables in the DataBase with the table schema from the migration files that are created.

```
python manage.py collectstatic
```
This command packages all the HTML, CSS and JS files in static folder

```
python manage.py createsuperuser
```
This command creates a superuser profile to access the admin page(http://localhost:8000/admin/)

```
python manage.py runserver
```
This command is used to start the server

## Testcases
API Level Testcases and Functional Testcases have been added.
Run the following command to run all the testcases:
```
pytest
```

## API Docs
To check the URL info:
```
GET - http://url-lookup-service-elb-692460868.ap-south-1.elb.amazonaws.com/urlinfo/1/{hostname_and_port}/{original_path_and_query_string}
```
Response Format:
```
{
    "host_name": "<host_name>",
    "port": <port>,
    "path": "<original_path>",
    "status": "malicious"
}
```

To list all URLs in the DataBase:
```
GET - http://url-lookup-service-elb-692460868.ap-south-1.elb.amazonaws.com/urlinfo/url/
```
Sample Response
```
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "url": "example.com",
            "is_restricted": true
        },
        {
            "id": 2,
            "url": "test.com",
            "is_restricted": true
        }
    ]
}
```

To add a new URL to the DataBase:
```
POST - http://url-lookup-service-elb-692460868.ap-south-1.elb.amazonaws.com/urlinfo/url/
```
Sample Request
```
{
    "url": "example.us"
}
```
Sample Response
```
{
    "status": "success",
    "message": "Inserted successfully"
}
```

To update an existing URL:
```
PUT - http://url-lookup-service-elb-692460868.ap-south-1.elb.amazonaws.com/urlinfo/url/
```
Sample Request
```
{
    "url_id": 1,
    "url": "example.ru"
}
```
Sample Response
```
{
    "status": "success",
    "message": "Updated successfully"
}
```
