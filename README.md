# awt-project-ws22-23-smart-learning-g1

## Pre-Requisites
### No installation required
GitHub Codespaces offer easy to use online development (https://github.com/features/codespaces).
To start a codespaces container click on code in the top right corner and start a codespace

### Quick installation
Install Docker desktop from https://www.docker.com/products/docker-desktop/

#### Manual installation
Follow the steps from https://docs.docker.com/engine/installation/linux/ubuntu/.

In my case, Docker CE has been installed.

Version check:
```shell
$ docker -v
Docker version 17.03.1-ce, build c6d412e
```

Follow the steps from https://docs.docker.com/compose/install/.
```shell
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.11.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
Apply executable permissions to the binary:
```shell
$ sudo chmod +x /usr/local/bin/docker-compose
```
Check the version:
```shell
$ docker-compose -v
docker-compose version 1.11.2, build dfed245
```
## Let it run
```shell
docker-compose up --build
```
## Links
* [Simple Flask SPA](https://www.bogotobogo.com/DevOps/Docker/Docker-Compose-FlaskREST-Service-Container-and-Apache-Container.php)
