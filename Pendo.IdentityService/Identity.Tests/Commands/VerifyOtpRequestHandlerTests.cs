using System.Linq.Expressions;
using FluentAssertions;
using Identity.DataAccess;
using Identity.DataAccess.Models;
using Identity.Schema.User.Auth;
using Identity.Util;
using Microsoft.Extensions.Logging;
using Moq;
using Pendo.IdentityService.Api.Commands;

namespace Identity.Tests.Commands;

[TestFixture]
public class VerifyOtpRequestHandlerTests
{
    private Mock<IJwtGenerator> _jwtGenerator;
    private Mock<IRepositoryFactory> _repositoryFactory;
    private Mock<IDateTimeProvider> _dateTimeProvider;
    private Mock<IOtpHasher> _otpHasher;
    private Mock<ILogger<VerifyOtpRequestHandler>> _logger;
    private VerifyOtpRequestHandler _handler;
    private DateTime _fixedTime;
    private Mock<IRepository<User>> _userRepo;
    private Mock<IRepository<OtpLogin>> _otpLoginRepo;

    [SetUp]
    public void Setup()
    {
        _jwtGenerator = new Mock<IJwtGenerator>();
        _repositoryFactory = new Mock<IRepositoryFactory>();
        _dateTimeProvider = new Mock<IDateTimeProvider>();
        _otpHasher = new Mock<IOtpHasher>();
        _logger = new Mock<ILogger<VerifyOtpRequestHandler>>();
        _fixedTime = new DateTime(2025, 2, 17, 12, 0, 0, DateTimeKind.Utc);
        _dateTimeProvider.Setup(x => x.UtcNow()).Returns(_fixedTime);
        _userRepo = new Mock<IRepository<User>>();
        _otpLoginRepo = new Mock<IRepository<OtpLogin>>();
        _repositoryFactory.Setup(x => x.Create<User>()).Returns(_userRepo.Object);
        _repositoryFactory.Setup(x => x.Create<OtpLogin>()).Returns(_otpLoginRepo.Object);
        _handler = new VerifyOtpRequestHandler(
            _jwtGenerator.Object,
            _repositoryFactory.Object,
            _logger.Object,
            _dateTimeProvider.Object,
            _otpHasher.Object);
    }

    [Test]
    public async Task Handle_WhenUserDoesNotExist_ReturnsFalse()
    {
        var request = new VerifyOtpRequest { EmailAddress = "mundrayj@gmail.com", Otp = "OTP_TOKEN" };
        _userRepo.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
            .ReturnsAsync([]);

        var response = await _handler.Handle(request);

        response.Authenticated.Should().BeFalse();
        response.Jwt.Should().BeEmpty();
    }

    [Test]
    public async Task Handle_WhenMultipleUsersExist_ReturnsFalse()
    {
        List<User> users = [new User { Email = "mundrayj@gmail.com", UserId = Guid.NewGuid() }, new User { Email = "mundrayj@gmail.com", UserId = Guid.NewGuid() }];
        var request = new VerifyOtpRequest { EmailAddress = "mundrayj@gmail.com", Otp = "OTP_TOKEN" };
        _userRepo.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
            .ReturnsAsync(users);

        var response = await _handler.Handle(request);

        response.Authenticated.Should().BeFalse();
        response.Jwt.Should().BeEmpty();
    }

    [Test]
    public async Task Handle_WhenOtpLoginNotFound_ReturnsFalse()
    {
        var user = new User { Email = "mundrayj@gmail.com", UserId = Guid.NewGuid() };
        var request = new VerifyOtpRequest { EmailAddress = "mundrayj@gmail.com", Otp = "OTP_TOKEN" };
        _userRepo.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
            .ReturnsAsync([user]);
        _otpLoginRepo.Setup(x => x.Read(It.IsAny<Expression<Func<OtpLogin, bool>>>()))
            .ReturnsAsync([]);

        var response = await _handler.Handle(request);

        response.Authenticated.Should().BeFalse();
        response.Jwt.Should().BeEmpty();
    }

    [Test]
    public async Task Handle_WhenOtpExpired_ReturnsFalse()
    {
        var user = new User { Email = "mundrayj@gmail.com", UserId = Guid.NewGuid() };
        var otpLogin = new OtpLogin
        {
            UserId = user.UserId,
            CodeHash = "HASH",
            HashSalt = "SALT",
            IssueDate = _fixedTime,
            ExpiryDate = _fixedTime.AddMinutes(-1)
        };

        var request = new VerifyOtpRequest { EmailAddress = "mundrayj@gmail.com", Otp = "OTP_TOKEN" };
        _userRepo.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
            .ReturnsAsync([user]);
        _otpLoginRepo.Setup(x => x.Read(It.IsAny<Expression<Func<OtpLogin, bool>>>()))
            .ReturnsAsync([otpLogin]);

        var response = await _handler.Handle(request);

        response.Authenticated.Should().BeFalse();
        response.Jwt.Should().BeEmpty();
    }

    [Test]
    public async Task Handle_WhenOtpInvalid_ReturnsFalse()
    {
        var user = new User { Email = "mundrayj@gmail.com", UserId = Guid.NewGuid() };
        var otpLogin = new OtpLogin
        {
            UserId = user.UserId,
            CodeHash = "HASH",
            HashSalt = "SALT",
            IssueDate = _fixedTime,
            ExpiryDate = _fixedTime.AddMinutes(5)
        };
        var request = new VerifyOtpRequest { EmailAddress = "mundrayj@gmail.com", Otp = "OTP_TOKEN" };
        _userRepo.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
            .ReturnsAsync([user]);
        _otpLoginRepo.Setup(x => x.Read(It.IsAny<Expression<Func<OtpLogin, bool>>>()))
            .ReturnsAsync([otpLogin]);
        _otpHasher.Setup(x => x.VerifyHash("OTP_TOKEN", "HASH", "SALT")).Returns(false);
        var response = await _handler.Handle(request);
        response.Authenticated.Should().BeFalse();
        response.Jwt.Should().BeEmpty();
    }

    [Test]
    public async Task Handle_WhenOtpValid_ReturnsTrueAndJwt()
    {
        var user = new User { Email = "mundrayj@gmail.com", UserId = Guid.NewGuid(), UserTypeId = 2 };
        var otpLogin = new OtpLogin
        {
            UserId = user.UserId,
            CodeHash = "HASH",
            HashSalt = "SALT",
            IssueDate = _fixedTime,
            ExpiryDate = _fixedTime.AddMinutes(5)
        };
        var request = new VerifyOtpRequest { EmailAddress = "mundrayj@gmail.com", Otp = "OTP_TOKEN" };

        _userRepo.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
            .ReturnsAsync([user]);
        _otpLoginRepo.Setup(x => x.Read(It.IsAny<Expression<Func<OtpLogin, bool>>>()))
            .ReturnsAsync([otpLogin]);
        _otpHasher.Setup(x => x.VerifyHash("OTP_TOKEN", "HASH", "SALT")).Returns(true);
        _otpLoginRepo.Setup(x => x.Update(It.IsAny<OtpLogin>(), true)).Returns(Task.CompletedTask);
        _otpLoginRepo.Setup(x => x.Read(It.IsAny<Expression<Func<OtpLogin, bool>>>()))
            .ReturnsAsync([otpLogin]);
        _jwtGenerator.Setup(x => x.GenerateJwt(It.IsAny<Guid>(), It.IsAny<string>(), true)).Returns("JWT_TOKEN");

        var response = await _handler.Handle(request);

        response.Authenticated.Should().BeTrue();
        response.Jwt.Should().Be("JWT_TOKEN");
        response.IsNewUser.Should().BeTrue();
    }
}
