import requests

class IdentityClient:
    """
    IdentityClient is a class that interacts with the Identity API.
    """
    
    def __init__(self, base_url, logger, jwt=None):
        self.base_url = base_url
        self.logger = logger
        self.jwt = jwt

    def _get_headers(self):
        headers = {}
        if self.jwt:
            token = f"Bearer {self.jwt}"
            headers["Authorization"] = token
            self.logger.debug(f"JWT header: {token}")
        return headers

    def RequestOtp(self, email):
        """
        RequestOtp sends a POST request to the Identity API to request an OTP.
        :param email: The email address to send the OTP to.
        :return: The response from the Identity API.
        """
        identityRequest = {"emailAddress": email}

        self.logger.info(f'Requesting OTP for {email}')
        self.logger.debug(f'Requesting OTP with payload: {identityRequest}')

        response = requests.post(
            f'{self.base_url}/api/Identity/RequestOtp',
            json=identityRequest,
            headers=self._get_headers(),
            verify=True
        )

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

        response = requests.post(
            f'{self.base_url}/api/Identity/VerifyOtp',
            json=request,
            headers=self._get_headers(),
            verify=True
        )

        self.logger.info(f'Received response from Identity API: {response.status_code}')
        self.logger.debug(f'Response payload: {response.text}')
        return response
    
    def Ping(self):
        """
        Ping sends a GET request to the Identity API to check if it is alive.
        :return: The response from the Identity API.
        """
        self.logger.info('Pinging Identity API')

        response = requests.get(
            f'{self.base_url}/api/Ping',
            headers=self._get_headers(),
            verify=True
        )

        self.logger.info(f'Received response from Identity API: {response.status_code}')
        self.logger.debug(f'Response payload: {response.text}')
        return response