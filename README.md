# assignment_mtfc

As mentioned in the assignment this project managing the basketball league, including teams, players, coaches, tournaments, and games The project also includes functionality for user authentication and permissions.

## Installation 
 python version -> Python 3.12.3


Clone the repository:
```
git clone <repository_url>
cd basketball_league
```

Create a virtual environment:
```
python -m venv venv
source venv/bin/activate 
```

Install dependencies:
```
pip install -r requirements.txt
```

Apply migrations:
```
python manage.py migrate
```


Create a superuser:
```
python manage.py createsuperuser
```


## Running Tests / Testcases 
```
python manage.py test
```

## Sample Data
 > 20 system users - admin(1), player(2), coach(18)
 > 17 Teams
 > 121 Players

 > 1 tournament 
 > 1 tournament Round
 > 8 Games 
 > 8 scores
 

```
python manage.py add_sample_data

```


## Running the Project
```
python manage.py runserver
```



Navigate to http://127.0.0.1:8000/




