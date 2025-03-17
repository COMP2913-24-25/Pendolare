import requests

class AdminClient:
    """
    AdminClient is a class that interacts with the Admin API.
    """

    def __init__(self, base_url, logger):
        self.base_url = base_url
        self.logger = logger

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

        response = requests.get(f'{self.base_url}/api/Admin/GetWeeklyRevenue', params=params, verify=True)

        self.logger.info(f'Received response from Admin API: {response.status_code}')
        self.logger.debug(f'Response payload: {response.text}')
        
        json_response = response.json()
        total_revenue = json_response.get('total', '')
        
        self.logger.info(f'Total Revenue: {total_revenue}')
        return total_revenue

    def UpdateBookingFee(self, fee):
        self.logger.info("Updating booking fee")
        payload = {"FeeMargin": float(fee)}
        response = requests.patch(f'{self.base_url}/api/UpdateBookingFee', json=payload, verify=True)
        self.logger.info(f"Update booking fee response: {response.status_code}")
        return response
