namespace Identity.Schema.User.Auth;

/// <summary>
/// Contains the JWT issued to the user.
/// </summary>
public class VerifyOtpResponse
{
    /// <summary>
    /// The JWT issued to the user.
    /// </summary>
    public required string Jwt;
}
