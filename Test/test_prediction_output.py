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
model_db = {
'rf_global': {
                'model': 'rf_global', 
                'score': '0.54',
                'branch': 'all'
                }, 
'lr_global': {
                'model': 'lr_global',
                'score': '0.61',
                'branch': 'all'
                },
'dt_global': {
                'model': 'dt_global',
                'score': '0.55',
                'branch': 'all'
                },
'rf_Disneyland_HongKong': {
                'model': 'rf_Disneyland_HongKong',
                'score': '0.48',
                'branch': 'Disneyland_HongKong'
                },
'rf_Disneyland_California': {
                'model': 'rf_Disneyland_California',
                'score': '0.65', 
                'branch': 'Disneyland_California'
                },
'rf_Disneyland_Paris': {
                'model': 'rf_Disneyland_Paris',
                'score': '0.45',
                'branch': 'Disneyland_Paris'}
}


for model in model_db:
    # requête
    model_name = str(model_db[model]['model'])
    model_score = str(model_db[model]['score'])
    comment = "Disneyland is a magical world!"
    username = 'bob'
    password = 'builder'
    r = requests.get(
        url='http://{address}:{port}/prediction'.format(address=api_address, port=api_port),
        auth=(username, password),
        params= {'model_name' : model_name,
                 'comment' : comment}
    )

    output = '''
    ============================
        get prediction test
    ============================
    | test date/time = {dt_string}

    request done at "/prediction"
    | username= {username}
    | password= {password}
    | model_name = {model_name}
    | comment = {comment}

    expected result = 5
    result = {request_score}

    ==>  {test_status}

    '''


    # statut de la requête
    request_score = r.json()['rating prediction']

    # affichage des résultats
    if request_score == '5':
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
    print(output.format(dt_string= dt_string, username=username, password=password, model_name=model_name,request_score = request_score, comment = comment, test_status=test_status))

    # impression dans un fichier
    
    if str(os.environ.get('LOG')) == '1':        
        with open('./results/log.txt', 'a') as file:
            file.write(output.format(dt_string= dt_string, username=username, password=password, model_name=model_name,request_score = request_score, comment = comment, test_status=test_status))

