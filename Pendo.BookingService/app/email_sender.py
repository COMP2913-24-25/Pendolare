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

    def SendBookingArrivalEmail(self, to, data):
        """
        SendBookingArrivalEmail method sends a booking arrival email to the specified recipient.
        :param to: Email address of the recipient.
        :param data: Data to be passed to the email template.
        :return: Response from SendGrid API.
        """
        return self._sendEmail(to, data, self.config.arrivalTemplateId)

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

        client = SendGridAPIClient(self.config.apiKey)
        response = client.send(message)
        return response
    
def generateEmailDataFromAmmendment(ammendment, driver, journey, vehicle):
    return {
        "booking_id": f"{ammendment.BookingId}",
        "driver_name": driver.FirstName if driver.FirstName is not None else "(Name not set)",
        "pickup_location": ammendment.StartName if ammendment.StartName is not None else journey.StartName,
        "pickup_time": ammendment.StartTime.strftime('%H:%M') if ammendment.StartTime is not None else journey.StartTime.strftime('%H:%M'),
        "pickup_date": journey.StartDate.strftime('%d/%m/%Y'),
        "dropoff_location": ammendment.EndName if ammendment.EndName is not None else journey.EndName,
        "vehicle_info": vehicle
    }

def generateEmailDataFromBooking(booking, driver, journey, vehicle):
    return {
        "booking_id": f"{booking.BookingId}",
        "driver_name": driver.FirstName if driver.FirstName is not None else "(Name not set)",
        "pickup_location": journey.StartName,
        "pickup_time": journey.StartTime.strftime('%H:%M'),
        "pickup_date": journey.StartDate.strftime('%d/%m/%Y'),
        "dropoff_location": journey.EndName,
        "vehicle_info": vehicle
    }