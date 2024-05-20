# assignment_mtfc

As mentioned in the assignment this project managing the basketball league, including teams, players, coaches, tournaments, and games The project also includes functionality for user authentication and permissions.

## Installation 
 python version -> Python 3.12.3 


Clone the repository:
```
git clone <repository_url>
cd assignment_mtfc
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


`Create a superuser(OPTIONAL):`
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



Navigate to http://127.0.0.1:8000/ test


### Login Credentials 

1. Player -> player1:player1
2. Admin - > admin:admin
3. Coach -> coach1:coach1

### API Explanation 

for API authenticatoin -> {baseURL}/api-auth/
 
 1. User (CRUD) (C: role = 'admin') `can see online users`
    - {baseURL}/api/stteams/users
    - {baseURL}/api/stteams/users/ <int:pk> /

 2. Teams (CRUD) (C: role = 'admin' , 'coach')
    - {baseURL}/api/stteams/teams
    - {baseURL}/api/stteams/teams/ <int:pk> /
    - {baseURL}/api/stteams/teams/ <int:pk> /top_players/

 3. Players (CRUD)  (C: role = 'admin', 'coach' )   
    - {baseURL}/api/stteams/players/
    - {baseURL}/api/stteams/players/ <int:pk> /

 4. Login Activities  (View only -> admin / user)
    -  {baseURL}/api/stteams/loginactivity/
    -  {baseURL}/api/stteams/loginactivity/ <int:pk> /


 5. Tournaments (CRUD) (C: admin only)
     - > once the Tournament is completed(all tournament rounds), you can see the Champian here
    -  {baseURL}/api/sttournaments/tournaments/
    -  {baseURL}/api/sttournaments/tournaments/ <int:pk> /

 6. Tournaments Rounds (CRUD) (C: admin only)  
    - > Only create the 1st round(with sample data its automatically created), based on the round teams score(Update Relavant Scores), other rounds are automatically generated. This API contains details for the dashboad.

        -  {basedURL}/api/sttournaments/tournamentrounds/
        -  {basedURL}/api/sttournaments/tournamentrounds/ <int:pk> /

 7. Games (CRUD) (C: admin only)
    -  {baseURL}/api/sttournaments/games
    -  {baseURL}/api/sttournaments/games/ <int:pk> /

 8. Scores (CURD) (C: admin only)  `Update the relavant scores to see the winners, Tournament Rounds and Tournament Champion - Automatically Updated`
    -  {baseURL}/api/sttournaments/scores
    -  {baseURL}/api/sttournaments/scores/ <int:pk> /






