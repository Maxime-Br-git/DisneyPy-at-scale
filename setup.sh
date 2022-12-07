cd Project/API
docker image build . -t disney_pred_api:latest

cd Project/Test
docker image build . -t test_img:latest

cd Project
docker-compose up