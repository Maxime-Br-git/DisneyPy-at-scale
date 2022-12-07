from fastapi import FastAPI, Response, Depends, HTTPException, Security, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from typing import Optional
import uvicorn
from auth_help import has_rights
from function import preprocess_text,load_model_db,get_prediction,get_score
import asyncio

api = FastAPI(
              title= "Disneyland review rating prediction API",
              description= "Use to predict the score of a customer based on his comment",
              version= "1.0.0",
              openapi_tags=[
    {
        'name': 'home',
        'description': 'welcome and confirm API is online'
    },
    {
        'name': 'performance',
        'description': 'functions that is used to inform user on model performance score'
    },
    {
        'name': 'prediction',
        'description': 'functions that is used to use one of the models to make a prediction'
    }

])


security = HTTPBasic()
available_model = ['rf_global','lr_global','dt_global','rf_Disneyland_HongKong','rf_Disneyland_California','rf_Disneyland_Paris']

@api.get('/', tags=['home'])
def get_index():
  """ 
  Welcome you and inform if API is online
  """
  return {'welcome to' : 'Disneyland review rating prediction API',
            'service status': 'Online'}

@api.get('/permission', tags=['home'])
async def credentials_validity(credentials: HTTPBasicCredentials = Depends(security)):
  """ 
  Use to test the validity of your credentials 
  """
  right = has_rights(credentials.username, credentials.password)
  
  if not right:
    raise HTTPException(
      status_code= status.HTTP_401_UNAUTHORIZED ,
      detail= "Could not validate credentials",
      headers= {"WWW-Authenticate": "Basic"},
    )
  else:
    return {'credentials' : 'valid'}

@api.get('/performance', tags=['performance'])

async def get_model_performance(model_name : str, credentials: HTTPBasicCredentials = Depends(security)):
  """
  inform the user on the model score on the testing set. Input **model_name** based on the following option :
* random forest on all branch => rf_global
* linear regression on all branch => lr_global
* decision tree on all branch => dt_global
* random forest on Disneyland hong kong => rf_Disneyland_HongKong
* random forest on Disneyland California  => rf_Disneyland_California
* random forest on Disneyland Paris  => rf_Disneyland_Paris
  
  (Authentification required)
  """
  right = has_rights(credentials.username, credentials.password)
  if not right:
    raise HTTPException(
      status_code= status.HTTP_401_UNAUTHORIZED ,
      detail= "Could not validate credentials",
      headers= {"WWW-Authenticate": "Basic"},
    )
  if model_name in available_model:
    return get_score(model_name)
  else:
    return {"please select an available model from the description list"}

@api.get('/prediction', tags=['prediction'])

async def get_model_prediction(model_name : str, comment : str, credentials: HTTPBasicCredentials = Depends(security)):
  """
  predict the model score base on the comment given by the user.
  ** PLEASE USE ENGLISH LANGUAGE TO WRITE DOWN THE COMMENT**
 Input **model_name** based on the following option :
* random forest on all branch => rf_global
* linear regression on all branch => lr_global
* decision tree on all branch => dt_global
* random forest on Disneyland hong kong => rf_Disneyland_HongKong
* random forest on Disneyland California  => rf_Disneyland_California
* random forest on Disneyland Paris  => rf_Disneyland_Paris
  
  (Authentification required)
  """
  right = has_rights(credentials.username , credentials.password)
  if not right:
    raise HTTPException(
      status_code= status.HTTP_401_UNAUTHORIZED ,
      detail= "Could not validate credentials",
      headers= {"WWW-Authenticate": "Basic"},
    )
  if model_name in available_model:
    if comment != "":
      return get_prediction(comment,model_name)
    else:
      return {"please add a comment"}
  else:
    return {"please select an available model from the description list"}
  
