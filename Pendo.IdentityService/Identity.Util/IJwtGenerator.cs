namespace Identity.Util;

/// <summary>
/// Generates Json Web Tokens to authenticate users.
/// </summary>
public interface IJwtGenerator
{
    /// <summary>
    /// Generates a new JWT.
    /// </summary>
    /// <param name="userId">The unique identifier for the user.</param>
    /// <param name="userEmail">The email of the user.</param>
    /// <param name="isManager">Boolean flag to indicate whether the user is a manager or not.</param>
    /// <returns></returns>
    string GenerateJwt(Guid userId, string userEmail, bool isManager);
}
