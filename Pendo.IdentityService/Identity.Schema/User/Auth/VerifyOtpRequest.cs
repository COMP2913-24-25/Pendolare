using System.ComponentModel.DataAnnotations;

namespace Identity.Schema.User.Auth;

public class VerifyOtpRequest : IRequest
{
    [EmailAddress]
    public required string Email { get; set; }
    public required string Otp { get; set; }
}
