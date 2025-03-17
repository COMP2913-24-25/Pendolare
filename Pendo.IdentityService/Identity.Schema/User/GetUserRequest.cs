namespace Identity.Schema.User;

/// <summary>
/// Used to get a user.
/// </summary>
public class GetUserRequest : IRequest
{
    /// <summary>
    /// The ID of the user.
    /// </summary>
    public Guid UserId { get; set; }
}