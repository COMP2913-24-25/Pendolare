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

    /// <summary>
    /// Indicates if the user is new and should have name etc. updated.
    /// </summary>
    public bool IsNewUser;

    /// <summary>
    /// Indicates whether the user was authenticated or not.
    /// </summary>
    public bool Authenticated;
}
