namespace Identity.Schema.User.Auth;

public class VerifyOtpRequest : IRequest
{
    public required string Otp { get; set; }
}
