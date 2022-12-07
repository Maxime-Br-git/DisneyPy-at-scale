FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests
RUN apt-get -y install curl
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD main.py main.py
ADD function.py function.py
ADD auth_help.py auth_help.py
ADD model.py model.py
ADD model/model_db.pickle /model/model_db.pickle
EXPOSE 8000
CMD uvicorn main:api --host 0.0.0.0 --port 8000