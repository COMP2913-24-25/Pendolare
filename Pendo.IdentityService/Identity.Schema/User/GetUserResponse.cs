namespace Identity.Schema.User;

/// <summary>
/// Returned when retrieving a user.
/// </summary>
public class GetUserResponse : Response
{
    /// <summary>
    /// The first name of the user.
    /// </summary>
    public string FirstName { get; set; } = string.Empty;

    /// <summary>
    /// The last name of the user.
    /// </summary>
    public string LastName { get; set; } = string.Empty;

    /// <summary>
    /// The rating of the user. -1 if no rating.
    /// </summary>
    public double UserRating { get; set; }
}
