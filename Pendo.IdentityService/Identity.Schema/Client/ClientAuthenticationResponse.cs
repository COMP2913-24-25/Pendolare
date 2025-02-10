using Identity.Util;

namespace Identity.Schema.Client;

/// <summary>
/// Represents the response returned after successful client authentication.
/// </summary>
public class ClientAuthenticationResponse
{
    /// <summary>
    /// Gets or sets the JSON Web Token (JWT) access token.
    /// </summary>
    public required string AccessToken { get; set; }

    /// <summary>
    /// Gets or sets the token type.
    /// </summary>
    public string TokenType { get; set; } = Constants.TokenType;

    /// <summary>
    /// Gets or sets the duration in seconds until the access token expires.
    /// </summary>
    public int ExpiresIn { get; set; }
}
