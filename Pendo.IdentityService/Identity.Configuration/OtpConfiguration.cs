namespace Identity.Configuration;

/// <summary>
/// Provides configuration for generating and sending OTP codes.
/// </summary>
public class OtpConfiguration
{
    /// <summary>
    /// Defines the length of the OTP codes. To be moved to DB config.
    /// </summary>
    public int OtpLength { get; set; } = 6;

    /// <summary>
    /// Provides the API Key for sending emails. To be moved to DB config.
    /// </summary>
    public required string SendGridApiKey { get; set; }

    /// <summary>
    /// The email to send OTP correspondence from.
    /// </summary>
    public required string SendGridFromEmail { get; set; }

    /// <summary>
    /// The template ID of the OTP email.
    /// </summary>
    public required string SendGridOtpTemplateId { get; set; }

    /// <summary>
    /// Number of minutes the code is valid for.
    /// </summary>
    public int ValidMinutes { get; set; } = 10;
}
