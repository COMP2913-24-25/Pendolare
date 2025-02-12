# 
# SHELL Script to deploy Pendo.PaymentService locally in a Docker Container
# Author: Alexander McCall
# Created: 12/02/2025
#

printf "\033[1m============================= Running Payment Service... ==============================\033[1m\n"

# remove any existing contains that are already running / exist using that image
printf "\033[1m============================= Removing Old Containers... ==============================\033[1m\n"

docker stop Pendo.PaymentService
docker rm -f Pendo.PaymentService

docker stop Pendo.PaymentService.Tests
docker rm -f Pendo.PaymentService.Tests

printf "\e[32mCompleted\e[0m\n"

# build fastapi image
printf "\033[1m============================= Building Docker Deploy Image ============================\033[1m\n"
docker build -f Dockerfile.deploy -t pendo.paymentservice.deploy.image .
printf "\033[1m Completed Deploy image \033[1m\n"

# build pytest image
printf "\033[1m============================= Building Docker Test Image ==============================\033[1m\n"
docker build -f Dockerfile.tests -t pendo.paymentservice.test.image .
printf "\033[1m Completed Tests image \033[1m\n"

# run automated tests
printf "\033[1m============================= Running Pytest ==========================================\033[1m\n"
docker run --name Pendo.PaymentService.Tests pendo.paymentservice.tests.image

# run service
printf "\033[1m============================= Running Pendo.PaymentService.Deploy =====================\033[1m\n"
docker run -d -p 5004:5004 --name Pendo.PaymentService pendo.paymentservice.deploy.image
printf "\e[32mContainer Created\e[0m\n"
printf "\e[32mPendo.PaymentService is running on localhost:5004\e[0m\n"