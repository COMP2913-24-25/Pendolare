namespace Identity.Configuration;

/// <summary>
/// Contains configuration for generating JWTs.
/// </summary>
public class JwtConfiguration
{
    /// <summary>
    /// The issuing party of the JWT (this app!!).
    /// </summary>
    public required string Issuer { get; set; }

    /// <summary>
    /// The audience value for the mobile app.
    /// </summary>
    public required string AppAudience { get; set; }

    /// <summary>
    /// The audience value for the manager dashboard.
    /// </summary>
    public required string ManagerAudience { get; set; }

    /// <summary>
    /// Secret signing key.
    /// </summary>
    public required string SecretKey { get; set; }

    /// <summary>
    /// Token expiry time.
    /// </summary>
    public int ExpiresInMinutes { get; set; } = 60;
}
