echo "|| Running Payment Service... ||"

# remove any existing contains that are already running / exist using that image
echo "Removing Docker Containers using old image..."
docker stop Pendo.PaymentService
docker rm -f Pendo.PaymentService
echo "Completed"

# build docker image
echo "Building Docker Image..."
docker build -t pendo.paymentservice.image .
echo "Image built"

# run new docker container with updated image
echo "Creating new Docker container..."
docker run -d -p 5004:5004 --name Pendo.PaymentService pendo.paymentservice.image
echo "Container created"
echo "Pendo.PaymentService is running on localhost:5004"
