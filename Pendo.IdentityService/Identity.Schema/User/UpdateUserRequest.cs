using System.ComponentModel.DataAnnotations;

namespace Identity.Schema.User;

/// <summary>
/// Request to update user data.
/// </summary>
public class UpdateUserRequest : IRequest
{
    /// <summary>
    /// The UserId of the user to update.
    /// </summary>
    public required Guid UserId { get; set; }

    /// <summary>
    /// The FirstName of the user to update.
    /// </summary>
    [Required]
    [Length(1, 255)]
    public required string FirstName { get; set; }

    /// <summary>
    /// The LastName of the user to update.
    /// </summary>
    [Required]
    [Length(1, 255)]
    public required string LastName { get; set; }
}
