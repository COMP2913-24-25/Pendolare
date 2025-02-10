using FluentAssertions;
using Identity.Util;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Identity.Tests.Util;

public class DateTimeProviderTests
{
    [Test]
    public void UtcNow_ReturnsTime()
    {
        IDateTimeProvider dateTimeProvider = new DateTimeProvider();

        dateTimeProvider.UtcNow().Should().BeCloseTo(DateTime.UtcNow, new TimeSpan(100));
    }
}
