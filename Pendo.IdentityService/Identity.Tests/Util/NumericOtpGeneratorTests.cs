using Identity.Configuration;
using Identity.Util;
using FluentAssertions;

namespace Identity.Tests.Util;

public class NumericOtpGeneratorTests
{
    [TestCase(1)]
    [TestCase(6)]
    [TestCase(20)]
    [TestCase(100)]
    public void GenerateToken_OfSetLength_ReturnsNumericCode(int otpLength)
    {
        IOtpGenerator generator = new NumericOtpGenerator(
            new SimpleOptions<OtpConfiguration>(
                new OtpConfiguration 
                { 
                    SendGridApiKey = "",
                    SendGridFromEmail = "",
                    SendGridOtpTemplateId = "",
                    OtpLength = otpLength
                }));

        generator.GenerateToken().Should()
            .NotBeNullOrEmpty().And
            .HaveLength(otpLength).And
            .MatchRegex(@$"^\d{{{otpLength}}}$");
    }
}
