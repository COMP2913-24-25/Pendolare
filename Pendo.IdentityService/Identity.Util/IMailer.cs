namespace Identity.Util;

/// <summary>
/// Used to send emails to users.
/// </summary>
public interface IMailer
{
    /// <summary>
    /// Sends an email to the address <param name="toMail"></param>
    /// </summary>
    Task<bool> Send(string toMail, object dynamicTemplateData);
}