
namespace Identity.Util;

/// <inheritdoc/>
public class DateTimeProvider : IDateTimeProvider
{
    public DateTime UtcNow() => DateTime.UtcNow;
}
