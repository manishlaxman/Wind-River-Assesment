# ENC-API

### Base requirements and Installation
Installing Python3
```sh
sudo apt update
sudo apt install python3 pip3
```

Installing Docker and Docker-Compose
```sh
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm -f get-docker.sh

sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

docker-compose start
```sh
cd /path/to/code/directory
docker-compose up -d
```

Run the API using kubernetes:
```sh
cd /path/to/code/directory
kubectl apply -f crypto-api-k8s.yml
```

Encrypt Data:
```sh
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"Input":"string"}' \
  http://localhost:80/api/encrypt
```

Decrypt Data:
```sh
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"Input":"encrypted-string"}' \
  http://localhost:80/api/decrypt
```

Get Health status:
```sh
curl --request GET http://localhost:80/api/health
```
