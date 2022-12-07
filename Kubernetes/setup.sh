#creation des images necessaire dans dockerhub
cd Project/API
docker tag 21ea3a461de8 brmaxime/project_mlops_api:latest
docker push brmaxime/project_mlops_api
docker tag 0d109cdc7d01 brmaxime/project_mlops_test:latest
docker push brmaxime/project_mlops_test

#installation de kubernetes
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

#lancement
minikube start
minikube dashboard --url=true

#install kubernetes console
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.21.0/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version --client
minikube addons enable ingress

#accéder au dashboard local 
kubectl proxy --address='0.0.0.0' --disable-filter=true

#create the service 
cd Project/Kubernetes
kubectl create -f my_api.yml
kubectl create -f my-ingress-project.yml
kubectl create -f my-service-project.yml
kubectl get ingress

ssh -i  C:\Users\Doudouz\datascientest\MLops\Keys\data_enginering_machine.pem  -L 8000:192.168.49.2:80 ubuntu@34.247.1.212