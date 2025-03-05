using System.ComponentModel.DataAnnotations;

namespace Identity.Schema.User.Auth;

/// <summary>
/// Used to request a One-time-passcode.
/// </summary>
public class OtpRequest : IRequest
{
    /// <summary>
    /// The email address to send the OTP to.
    /// </summary>
    [EmailAddress(ErrorMessage = "User must enter a valid email.")]
    public required string EmailAddress { get; set; }
}
