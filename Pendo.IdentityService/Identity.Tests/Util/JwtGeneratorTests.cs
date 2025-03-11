using FluentAssertions;
using Identity.Util;
using Identity.Configuration;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.JsonWebTokens;
using Microsoft.IdentityModel.Tokens;
using System.Security.Claims;
using Moq;
using System.Text;

namespace Identity.Tests.Util;

[TestFixture]
public class JwtGeneratorTests
{
    private JwtGenerator _jwtGenerator;
    private JwtConfiguration _config;
    private Mock<IDateTimeProvider> _dateTimeProvider;

    [SetUp]
    public void Setup()
    {
        _config = new JwtConfiguration
        {
            SecretKey = "mmmmmyesverysecret12352346789543468986421243578965432134679i",
            Issuer = "testIssuer",
            AppAudience = "testAudience",
            ManagerAudience = "testManagerAudience",
            ExpiresInMinutes = 60
        };

        _dateTimeProvider = new Mock<IDateTimeProvider>();
        _dateTimeProvider.Setup(d => d.UtcNow()).Returns(new DateTime(2025, 02, 17));

        _jwtGenerator = new JwtGenerator(Options.Create(_config), _dateTimeProvider.Object);
    }

    [Test]
    public void GenerateJwt_ShouldReturnValidToken()
    {
        string userEmail = "mundrayj@gmail.com";
        bool isManager = false;

        string token = _jwtGenerator.GenerateJwt(userEmail, isManager);

        token.Should().NotBeNullOrEmpty();
    }

    [Test]
    public async Task GenerateJwt_ShouldContainCorrectClaims()
    {
        string userEmail = "mundrayj@gmail.com";
        bool isManager = true;

        string token = _jwtGenerator.GenerateJwt(userEmail, isManager);
        var handler = new JsonWebTokenHandler();
        var validationParams = new TokenValidationParameters
        {
            ValidateIssuer = false,
            ValidateAudience = false,
            ValidateIssuerSigningKey = false,
            ValidateLifetime = false,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_config.SecretKey))
        };

        var result = await handler.ValidateTokenAsync(token, validationParams);

        result.IsValid.Should().BeTrue();
        result.Claims[ClaimTypes.Name].Should().Be(userEmail);
        result.Claims[Constants.UserTypeClaim].Should().Be(Constants.Manager);
    }
}
