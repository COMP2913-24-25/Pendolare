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
        return headers

    def GetWeeklyRevenue(self, start_date, end_date):
        self.logger.info('Getting weekly revenue')
        params = {
            'StartDate': start_date.strftime('%Y-%m-%d'),
            'EndDate': end_date.strftime('%Y-%m-%d')
        }
        response = requests.get(f'{self.base_url}/api/Admin/GetWeeklyRevenue', params=params, headers=self._get_headers(), verify=True)
        self.logger.info(f'Received response from Admin API: {response.status_code}')
        self.logger.debug(f'Response payload: {response.text}')
        json_response = response.json()
        self.logger.info(f'Full revenue response: {json_response}')
        return json_response

    def UpdateBookingFee(self, fee):
        self.logger.info("Updating booking fee")
        payload = {"FeeMargin": float(fee) / 100.0}
        # Print payload with extra spacing for clarity
        self.logger.debug("Payload for UpdateBookingFee: \n%s\n", payload)
        response = requests.patch(f'{self.base_url}/api/Admin/UpdateBookingFee', json=payload, headers=self._get_headers(), verify=True)
        self.logger.info(f"Update booking fee response: {response.status_code}")
        return response

    def GetBookingFee(self):
        self.logger.info("Getting booking fee")
        response = requests.get(f'{self.base_url}/api/Admin/GetBookingFee', headers=self._get_headers(), verify=True)
        if response.status_code == 200:
            fee = response.json().get("BookingFee", "0.00%")
            self.logger.info(f"Booking fee: {fee}")
            return fee
        else:
            self.logger.error(f"Failed to get booking fee: {response.status_code}")
            return "0.00%"

    def GetDiscounts(self):
        self.logger.info("Getting discounts")
        response = requests.get(f'{self.base_url}/api/Admin/Discounts', headers=self._get_headers(), verify=True)
        self.logger.info(f"Discounts response: {response.status_code}")
        return response.json() if response.status_code == 200 else []

    def CreateDiscount(self, weekly_journeys, discount_percentage):
        self.logger.info("Creating discount")
        payload = {"WeeklyJourneys": weekly_journeys, "DiscountPercentage": discount_percentage}
        # Print payload with extra spacing for clarity
        self.logger.debug("Payload for CreateDiscount: \n%s\n", payload)
        response = requests.post(f'{self.base_url}/api/Admin/CreateDiscount', json=payload, headers=self._get_headers(), verify=True)
        self.logger.info(f"Create discount response: {response.status_code}")
        return response.json() if response.status_code == 200 else None

    def DeleteDiscount(self, discount_id):
        self.logger.info("Deleting discount with id: %s", discount_id)
        response = requests.delete(f'{self.base_url}/api/Admin/Discounts/{discount_id}', headers=self._get_headers(), verify=True)
        self.logger.info("Delete discount response: %s", response.status_code)
        return response.status_code == 200
