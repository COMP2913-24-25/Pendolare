using System.ComponentModel.DataAnnotations;

namespace Identity.Schema.Client;

/// <summary>
/// Represents a client authentication request using client credentials.
/// </summary>
public class ClientAuthenticationRequest : IRequest
{
    /// <summary>
    /// Gets or sets the client identifier.
    /// </summary>
    [Required(ErrorMessage = "ClientId is required.")]
    [StringLength(100, MinimumLength = 3, ErrorMessage = "ClientId must be between 3 and 100 characters.")]
    public required string ClientId { get; set; }

    /// <summary>
    /// Gets or sets the client secret.
    /// </summary>
    [Required(ErrorMessage = "ClientSecret is required.")]
    [StringLength(100, MinimumLength = 6, ErrorMessage = "ClientSecret must be between 6 and 100 characters.")]
    public required string ClientSecret { get; set; }
}