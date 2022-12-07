### AUG22MLOPS_Maxime_Brendel

# API (Project/API)

Explaination of the structure and content :

- Api is located on the main.py file 

- Files were created to avoid monolithical code and enable unit testing as much as possible :
    - Auth_help.py is used to handle user login with base64 encryption
    - Functions.py is used to pull the relevant information from the model that was saved in the pickle file (./model/model_db.pickle)
    - modeL.py for readability of the scheme 
    - all ML models preprocessing and training has been done and saved within a pickle file using the ./model/ML_model.py
    - docker image was created using the Dockerfile and push to brmaxime/project_mlops_api:latest

- API access : broadcasting on localhost port 8000

- For details on API please use the <yourIP>:8000/docs after running the image within docker as all path usage is details within the API documentation  (use credentials : id=>bob , pwd=>builder to test it out)

# Testing the API stability using docker-compose file: 

- in the folder ./Project/Test is located the python file that will test the API container on the following conditions:
    - test of valid permission ==> ensure the valid credentials give access to the api
    - test of invalid permission ==> ensure invalid credentials refuse access to the api
    - test of algorithms performance visibility ==> ensure all algorithms present give the correct score 
    - test of algorithms output ==> ensure each of the 6 algorithms give an 5 star rating output for a positive comment 

- all tests are compiled into a docker image located at brmaxime/test:latest
- results of the tests are compiled in a text file in ./Project/Test/results.txt with the date and time when it was executed

- To run the tests use the docker-compose.yml located in ./Project. Note you will need to change the IP_ADRESS environment variable to the IP of the machine you run the container on. 

# Deploy using Kubernetes for stability and load balancing : 

- A cluster of 3 pods running the API container has been created to ensure a larger amount of query on the API without losing the service
-  To setup and run the service you can follow the setup.sh file located in the kubernetes folder . Note you will need to change the IP_ADRESS environment variable to the IP of the machine you run the container on. 

Please adapt the last command to : ssh -i  yourVMkey.pem  -L 8000:192.168.49.2:80 ubuntu@<yourVMIP> to broadcast on your local machine at port 8000