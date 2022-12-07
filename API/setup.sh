pip3 install fastapi uvicorn Fastapi
pip3 install pandas numpy nltk
pip3 install sklearn

pip3 freeze > requirements.txt 

#for initial installation 
sudo service docker start

cd /Project/API
docker image build . -t disney_pred_api:latest
docker run -d --name api_container -p 8000:8000 disney_pred_api:latest