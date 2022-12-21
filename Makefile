start:
	docker-compose up -d
down:
	docker-compose down --rmi local --remove-orphans

install:
	sudo groupadd docker
	sudo usermod -aG docker $USER
	sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose