using FluentAssertions;
using Identity.Util;

namespace Identity.Tests.Util;

public class DateTimeProviderTests
{
    [Test]
    public void UtcNow_ReturnsTime()
    {
        IDateTimeProvider dateTimeProvider = new DateTimeProvider();

        dateTimeProvider.UtcNow().Should().BeCloseTo(DateTime.UtcNow, new TimeSpan(0, 1, 0));
    }
}
