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

    def SendPayoutEmail(self, to, data):
        """
        SendPayoutEmail method sends a payout email to the specified recipient(s).
        :param to: Email address of the recipient.
        :param data: Data to be passed to the email template.
        :return: Response from SendGrid API.
        """
        return self._sendEmail(to, data, self.config.payoutTemplateId)

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
    
def generateEmailData(driver, nonPending):
    return {
        "driver_name": driver.FirstName if driver.FirstName is not None else "(Name not set)",
        "non_pending": float(nonPending)
    }