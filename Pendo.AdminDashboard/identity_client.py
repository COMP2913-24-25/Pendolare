import requests

class IdentityClient:
    """
    IdentityClient is a class that interacts with the Identity API.
    """
    
    def __init__(self, base_url, logger):
        self.base_url = base_url
        self.logger = logger

    def RequestOtp(self, email):
        """
        RequestOtp sends a POST request to the Identity API to request an OTP.
        :param email: The email address to send the OTP to.
        :return: The response from the Identity API.
        """
        identityRequest = {"emailAddress": email}

        self.logger.info(f'Requesting OTP for {email}')
        self.logger.debug(f'Requesting OTP with payload: {identityRequest}')

        response = requests.post(f'{self.base_url}/api/Auth/RequestOtp', json=identityRequest, verify=True)

        self.logger.info(f'Received response from Identity API: {response.status_code}')
        self.logger.debug(f'Response payload: {response.text}')
        return response
    
    def VerifyOtp(self, email, otp):
        """
        VerifyOtp sends a POST request to the Identity API to verify an OTP.
        :param email: The email address to verify the OTP for.
        :param otp: The OTP to verify.
        :return: The response from the Identity API.
        """
        request = {"emailAddress": email, "otp": otp}

        self.logger.info(f'Verifying OTP for {email}')
        self.logger.debug(f'Verifying OTP with payload: {request}')

        response = requests.post(f'{self.base_url}/api/Auth/VerifyOtp', json=request, verify=True)

        self.logger.info(f'Received response from Identity API: {response.status_code}')
        self.logger.debug(f'Response payload: {response.text}')
        return response
    
    def Ping(self):
        """
        Ping sends a GET request to the Identity API to check if it is alive.
        :return: The response from the Identity API.
        """
        self.logger.info('Pinging Identity API')

        response = requests.get(f'{self.base_url}/api/Ping', verify=True)

        self.logger.info(f'Received response from Identity API: {response.status_code}')
        self.logger.debug(f'Response payload: {response.text}')
        return response