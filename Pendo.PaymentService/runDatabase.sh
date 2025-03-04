# 
# SHELL Script to deploy Pendo.Database locally in an MSSQL Docker Container on port 1433
# Author: Alexander McCall
# Created: 16/02/2025
#

printf "\033[1m============================= Running Pendo.Database... ==============================\033[1m\n"

# remove any existing contains that are already running / exist using that image
printf "\033[1m============================= Removing Old Containers... ==============================\033[1m\n"

docker stop Pendo.Database
docker rm -f Pendo.Database

printf "\e[32mCompleted\e[0m\n"

# run database
printf "\033[1m============================= Running Pendo.Database =====================\033[1m\n"
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=reallyStrongPwd123" -p 1433:1433 --name Pendo.Database --hostname Pendo.Database  -d mcr.microsoft.com/mssql/server:2022-latest

printf "\e[32mContainer Created\e[0m\n"
printf "\e[32mPendo.Database is running on localhost:1433\e[0m\n"
printf "\e[32mPendo.Database Username: SA, Password: reallyStrongPwd123\e[0m\n"

# update PendoDatabase.py with sqlacodegen to create sqlalchemy python file based off database schema
#printf "\033[1m============================= Updating PendoDatabase.py =====================\033[1m\n"
#sqlacodegen_v2 --schema identity,payment,shared  mssql+pymssql://SA:reallyStrongPwd123@localhost:1433/Pendo.Database > PendoDatabase.py