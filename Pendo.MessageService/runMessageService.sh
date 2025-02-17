# 
# SHELL Script to deploy Pendo.MessageService locally in a Docker Container
# Author: Alexander McCall & Lara Glenn
# Created: 12/02/2025
#

printf "\033[1m============================= Running Payment Service... ==============================\033[1m\n"

# remove any existing contains that are already running / exist using that image
printf "\033[1m============================= Removing Old Containers... ==============================\033[1m\n"

docker stop Pendo.MessageService
docker rm -f Pendo.MessageService

docker stop Pendo.MessageService.Tests
docker rm -f Pendo.MessageService.Tests

printf "\e[32mCompleted\e[0m\n"

# build fastapi image
printf "\033[1m============================= Building Docker Deploy Image ============================\033[1m\n"
docker build -f Dockerfile.deploy -t pendo.messageservice.deploy.image .
printf "\033[1m Completed Deploy image \033[1m\n"

# build pytest image
printf "\033[1m============================= Building Docker Test Image ==============================\033[1m\n"
docker build -f Dockerfile.tests -t pendo.messageservice.test.image .
printf "\033[1m Completed Tests image \033[1m\n"

# run automated tests
printf "\033[1m============================= Running Pytest ==========================================\033[1m\n"
docker run --name Pendo.MessageService.Tests pendo.messageservice.test.image

# run service
printf "\033[1m============================= Running Pendo.MessageService.Deploy =====================\033[1m\n"
docker run -d -p 5006:5006 --name Pendo.MessageService pendo.messageservice.deploy.image
printf "\e[32mContainer Created\e[0m\n"
printf "\e[32mPendo.MessageService is running on localhost:5006\e[0m\n"