## App to obtain movies and actors info from themoviedb.org

You have to obtain bearer token in order to use the app. To register for an API
key, click the link from within your account settings page
https://www.themoviedb.org/settings/api.

- Clone project, set up virtual environment and install project dependencies 
  (code depends on your OS):
```
$ python -m venv venv
$ source ./venv/scripts/activate
$ pip install -r requirements.txt
```

- To set your bearer token run the following line:
```
$ export 'BEARER_TOKEN'='<your_bearer_token>'
```

- Run app with one of two parameters:

*Provide -n or --number parameter with integer number to get movies:*
```
$ python tmdb.py -n 5
```

*Provide -i or --id parameter with integer movie's id to get it actors:*
```
$ python tmdb.py --id 385128
```