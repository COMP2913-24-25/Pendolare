using System.ComponentModel.DataAnnotations;

namespace Identity.Schema.User.Auth;

/// <summary>
/// Request used to verify one-time codes.
/// </summary>
public class VerifyOtpRequest : IRequest
{
    /// <summary>
    /// The email address of the user.
    /// </summary>
    [Required]
    [EmailAddress(ErrorMessage = "User must enter a valid email.")]
    public required string EmailAddress { get; set; }

    /// <summary>
    /// The one-time code to verify.
    /// </summary>
    [Required]
    public required string Otp { get; set; }
}
