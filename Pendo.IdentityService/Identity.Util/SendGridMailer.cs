using Identity.Configuration;
using Microsoft.Extensions.Options;
using SendGrid;
using SendGrid.Helpers.Mail;
using System.Net;

namespace Identity.Util;

/// <inheritdoc/>
public class SendGridMailer : IMailer
{
    private readonly OtpConfiguration _config;

    public SendGridMailer(IOptions<OtpConfiguration> options)
    {
        _config = options.Value;
    }

    public async Task<bool> Send(string toMail, object dynamicTemplateData)
    {
        var client = new SendGridClient(_config.SendGridApiKey);
        var from = new EmailAddress(_config.SendGridFromEmail);
        var message = new SendGridMessage
        {
            From = from,
            TemplateId = _config.SendGridOtpTemplateId
        };

        message.SetTemplateData(dynamicTemplateData);
        message.AddTo(toMail);

        var response = await client.SendEmailAsync(message);

        return response.StatusCode is HttpStatusCode.OK or HttpStatusCode.Accepted;
    }
}
