from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class MailSender:
    """
    MailSender class is responsible for sending emails using SendGrid API.
    """

    def __init__(self, sendgrid_configuration):
        """
        Constructor for MailSender class.
        :param sendgrid_configuration: Configuration object for SendGrid.
        """
        self.config = sendgrid_configuration

    def SendBookingConfirmation(self, to, data):
        """
        SendBookingConfirmation method sends a booking confirmation email to the specified recipient.
        :param to: Email address of the recipient.
        :param data: Data to be passed to the email template.
        :return: Response from SendGrid API.
        """
        return self._sendEmail(to, data, self.config.confirmedTemplateId)
    
    def SendBookingPending(self, to, data):
        """
        SendBookingPending method sends a booking pending email to the specified recipient.
        :param to: Email address of the recipient.
        :param data: Data to be passed to the email template.
        :return: Response from SendGrid API.
        """
        return self._sendEmail(to, data, self.config.pendingTemplateId)
    
    def SendBookingCancelled(self, to, data):
        """
        SendBookingCancelled method sends a booking cancelled email to the specified recipient.
        :param to: Email address of the recipient.
        :param data: Data to be passed to the email template.
        :return: Response from SendGrid API.
        """
        return self._sendEmail(to, data, self.config.cancelledTemplateId)

    def _sendEmail(self, to, data, template_id):
        """
        SendEmail method sends an email to the specified recipient.
        :param to: Email address of the recipient.
        :param data: Data to be passed to the email template.
        :return: Response from SendGrid API.
        """
        message = Mail(
            from_email=self.config.fromEmail,
            to_emails=to)
        message.template_id = template_id
        message.dynamic_template_data = data
        try:
            client = SendGridAPIClient(self.config.apiKey)
            response = client.send(message)
            return response
        except Exception as e:
            return str(e)
        
def generateEmailDataFromAmmendment(ammendment, driver, journey):
    return{
        "booking_id": f"{ammendment.BookingId}",
        "driver_name": driver.FirstName if driver.FirstName is not None else "(Name not set)",
        "pickup_location": ammendment.StartName if ammendment.StartName is not None else journey.StartName,
        "pickup_time": ammendment.StartTime.time() if ammendment.StartTime is not None else journey.StartTime.time(),
        "pickup_date": journey.StartDate.date(),
        "dropoff_location": ammendment.EndName if ammendment.EndName is not None else journey.EndName,
        "vehicle_info": "Mazda MX-5 Blue"
    }

def generateEmailDataFromBooking(booking, driver, journey):
    return{
        "booking_id": f"{booking.BookingId}",
        "driver_name": driver.FirstName if driver.FirstName is not None else "(Name not set)",
        "pickup_location": journey.StartName,
        "pickup_time": journey.StartTime.time(),
        "pickup_date": journey.StartDate.date(),
        "dropoff_location": journey.EndName,
        "vehicle_info": "Mazda MX-5 Blue"
    }