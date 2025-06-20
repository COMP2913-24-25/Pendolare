import requests

class VehicleEnquiryClient:
    """
    VehicleEnquiryClient is a client for the DVLA vehicle enquiry API.
    """
    def __init__(self, api_key, logger):
        self.api_key = api_key
        self.logger = logger
        self.path = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"
        self.headers = {
            "x-api-key" : api_key,
            "Content-Type" : "application/json"
        }

    def GetVehicleDetails(self, registration):
        """
        GetVehicleDetails method sends a request to the DVLA vehicle enquiry API to get vehicle details.
        """
        request = {"registrationNumber": registration}

        self.logger.debug(f"Vehicle enquiry request: {request}")

        response = requests.post(self.path, headers=self.headers, json=request)
        response_data = response.json()

        self.logger.debug(f"Vehicle enquiry response: {response_data}")

        if 'errors' in response_data:
            self.logger.info(f"Vehicle '{registration}' not found")
            return f"Unknown ({registration})"
        
        return self._formatResponse(response_data)

    def _formatResponse(self, response_data):
        """
        _formatResponse method formats the response from the DVLA vehicle enquiry API.
        """
        reg = response_data['registrationNumber']
        make = response_data['make'].capitalize()
        colour = '' if 'colour' not in response_data else response_data['colour'].capitalize()

        return f"{colour} {make} ({reg})"