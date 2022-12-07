import os
import requests
from datetime import datetime
 

# dd/mm/YY H:M:S
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# définition de l'adresse de l'API
api_address = str(os.environ.get('IP_ADRESS'))
# api_address = '34.247.1.212'
# port de l'API
api_port = str(os.environ.get('IP_PORT'))
# api_port = '8000'

#user_db
users_db = {
    "alice": {
        "username": "alice",
        "password": "John Doe"
    },
    "bob": {
        "username": "bob",
        "password": "builder"
    },
    "clementine": {
        "username": "clementine",
        "password": "mandarine"
    },
    "admin": {
        "username": "admin",
        "password": "4dm1N"
    },
}


for user in users_db:
    # requête
    username = str(users_db[user]['username'])
    password = str(users_db[user]['password'])
    r = requests.get(
        url='http://{address}:{port}/permission'.format(address=api_address, port=api_port),
        auth=(username, password)
    )

    output = '''
    ============================
        Authentication test
    ============================
    | test date/time = {dt_string}

    request done at "/permission"
    | username= {username}
    | password= {password}

    expected result = 200
    actual restult = {status_code}

    ==>  {test_status}

    '''


    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code == 200:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
    print(output.format(dt_string= dt_string, username=username, password=password, status_code=status_code, test_status=test_status))

    # impression dans un fichier
    if str(os.environ.get('LOG')) == '1':        
        with open('./results/log.txt', 'a') as file:
            file.write(output.format(dt_string= dt_string, username=username, password=password, status_code=status_code, test_status=test_status))

