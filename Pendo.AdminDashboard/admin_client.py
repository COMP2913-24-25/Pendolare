import requests

class AdminClient:
    """
    AdminClient is a class that interacts with the Admin API.
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
            # Removed logging of the JWT to prevent exposing sensitive information:
            # self.logger.debug(f"JWT header: {token}")
        return headers

    def GetWeeklyRevenue(self, start_date, end_date):
        """
        GetWeeklyRevenue sends a GET request to the Admin API to get the weekly revenue.
        :param start_date: The start date of the week.
        :param end_date: The end date of the week.
        :return: The response from the Admin API.
        """
        self.logger.info('Getting weekly revenue')

        params = {
            'StartDate': start_date.strftime('%Y-%m-%d'),
            'EndDate': end_date.strftime('%Y-%m-%d')
        }

        response = requests.get(f'{self.base_url}/api/Admin/GetWeeklyRevenue',
                                params=params,
                                headers=self._get_headers(),
                                verify=True)

        self.logger.info(f'Received response from Admin API: {response.status_code}')
        self.logger.debug(f'Response payload: {response.text}')
        
        json_response = response.json()
        
        self.logger.info(f'Full revenue response: {json_response}')
        return json_response

    def UpdateBookingFee(self, fee):
        self.logger.info("Updating booking fee")
        payload = {"FeeMargin": float(fee) / 100.0}  # convert percentage to decimal as expected by UpdateBookingFeeCommand
        response = requests.patch(f'{self.base_url}/api/Admin/UpdateBookingFee',
                                  json=payload,
                                  headers=self._get_headers(),
                                  verify=True)
        self.logger.info(f"Update booking fee response: {response.status_code}")
        return response

    def GetBookingFee(self):
        self.logger.info("Getting booking fee")
        response = requests.get(f'{self.base_url}/api/Admin/GetBookingFee',
                                headers=self._get_headers(),
                                verify=True)
        if response.status_code == 200:
            fee = response.json().get("BookingFee", "0.00%")  # changed key to "BookingFee"
            self.logger.info(f"Booking fee: {fee}")
            return fee
        else:
            self.logger.error(f"Failed to get booking fee: {response.status_code}")
            return "0.00%"
