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
        """Fetch weekly revenue for the given date range.

        :param start_date: Start date as a datetime object.
        :param end_date: End date as a datetime object.
        :return: JSON response with revenue details.
        """
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
        """Updates the booking fee margin.

        :param fee: Fee value as a percentage.
        :return: Response object from the Admin API.
        """
        self.logger.info("Updating booking fee")
        payload = {"FeeMargin": float(fee) / 100.0}
        response = requests.patch(f'{self.base_url}/api/Admin/UpdateBookingFee', json=payload, headers=self._get_headers(), verify=True)
        self.logger.info(f"Update booking fee response: {response.status_code}")
        return response

    def GetBookingFee(self):
        """Retrieves the current booking fee.

        :return: Booking fee as a string.
        """
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
        """Fetch available discounts from the Admin API.

        :return: List of discounts.
        """
        self.logger.info("Getting discounts")
        response = requests.get(f'{self.base_url}/api/Admin/Discounts', headers=self._get_headers(), verify=True)
        self.logger.info(f"Discounts response: {response.status_code}")
        return response.json() if response.status_code == 200 else []

    def CreateDiscount(self, weekly_journeys, discount_percentage):
        """Creates a discount using given parameters.

        :param weekly_journeys: Applicable weekly journey count.
        :param discount_percentage: Discount percentage.
        :return: JSON response if creation is successful, otherwise None.
        """
        self.logger.info("Creating discount")
        payload = {"WeeklyJourneys": weekly_journeys, "DiscountPercentage": discount_percentage}
        response = requests.post(f'{self.base_url}/api/Admin/CreateDiscount', json=payload, headers=self._get_headers(), verify=True)
        self.logger.info(f"Create discount response: {response.status_code}")
        return response.json() if response.status_code == 200 else None

    def DeleteDiscount(self, discount_id):
        """Deletes a discount identified by discount_id.

        :param discount_id: The ID of the discount to delete.
        :return: True if deletion is successful, otherwise False.
        """
        self.logger.info("Deleting discount with id: %s", discount_id)
        response = requests.delete(f'{self.base_url}/api/Admin/Discounts/{discount_id}', headers=self._get_headers(), verify=True)
        self.logger.info("Delete discount response: %s", response.status_code)
        return response.status_code == 200
