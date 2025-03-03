# 
# SHELL Script to deploy Pendo.JourneyService locally in a Docker Container
# Author: Alexander McCall
# Created: 12/02/2025
#

printf "\033[1m============================= Running Journey Service... ==============================\033[1m\n"

# remove any existing contains that are already running / exist using that image
printf "\033[1m============================= Removing Old Containers... ==============================\033[1m\n"

docker stop Pendo.JourneyService
docker rm -f Pendo.JourneyService

#docker stop Pendo.JourneyService.Tests
#docker rm -f Pendo.JourneyService.Tests

printf "\e[32mCompleted\e[0m\n"

# build fastapi image
printf "\033[1m============================= Building Docker Deploy Image ============================\033[1m\n"
docker build -f Dockerfile.deploy -t pendo.journeyservice.deploy.image .
printf "\033[1m Completed Deploy image \033[1m\n"

# build pytest image
printf "\033[1m============================= Building Docker Test Image ==============================\033[1m\n"
#docker build -f Dockerfile.tests -t pendo.journeyservice.test.image .
printf "\033[1m Completed Tests image \033[1m\n"

# run automated tests
#printf "\033[1m============================= Running Pytest ==========================================\033[1m\n"
#docker run --name Pendo.JourneyService.Tests pendo.journeyservice.test.image

# run service
printf "\033[1m============================= Running Pendo.JourneyService.Deploy =====================\033[1m\n"
docker run -d -p 5002:5002 --name Pendo.JourneyService pendo.journeyservice.deploy.image
printf "\e[32mContainer Created\e[0m\n"
printf "\e[32mPendo.JourneyService is running on localhost:5002\e[0m\n"