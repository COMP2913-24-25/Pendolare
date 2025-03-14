namespace Identity.Util;

/// <summary>
/// Wrapper to provide the current time.
/// </summary>
public interface IDateTimeProvider
{
    /// <summary>
    /// Gets a UTC representation of the current time.
    /// </summary>
    DateTime UtcNow();
}
