using System.Linq.Expressions;
using FluentAssertions;
using Identity.Configuration;
using Identity.DataAccess;
using Identity.DataAccess.Models;
using Identity.Schema;
using Identity.Schema.User.Auth;
using Identity.Util;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Moq;
using Pendo.IdentityService.Api.Commands;

namespace Identity.Tests.Commands;

[TestFixture]
public class OtpRequestHandlerTests
{
    private Mock<IMailer> _mailer;
    private Mock<IOtpGenerator> _otpGenerator;
    private Mock<IRepositoryFactory> _repositoryFactory;
    private Mock<IDateTimeProvider> _dateTimeProvider;
    private Mock<IOtpHasher> _otpHasher;
    private Mock<ILogger<OtpRequestHandler>> _logger;
    private IOptions<OtpConfiguration> _otpOptions;
    private IOptions<ManagerConfiguration> _managerOptions;
    private OtpRequestHandler _handler;
    private DateTime _fixedTime;
    private Mock<IRepository<User>> _userRepo;
    private Mock<IRepository<OtpLogin>> _otpLoginRepo;

    [SetUp]
    public void Setup()
    {
        _mailer = new Mock<IMailer>();
        _otpGenerator = new Mock<IOtpGenerator>();
        _repositoryFactory = new Mock<IRepositoryFactory>();
        _dateTimeProvider = new Mock<IDateTimeProvider>();
        _otpHasher = new Mock<IOtpHasher>();
        _logger = new Mock<ILogger<OtpRequestHandler>>();
        _fixedTime = new DateTime(2025, 2, 17, 12, 0, 0, DateTimeKind.Utc);
        _dateTimeProvider.Setup(x => x.UtcNow()).Returns(_fixedTime);
        _otpOptions = Options.Create(new OtpConfiguration { ValidMinutes = 5, SendGridApiKey = "", SendGridFromEmail = "", SendGridOtpTemplateId = "" });
        _managerOptions = Options.Create(new ManagerConfiguration { Whitelist = ["manager@test.com"] });
        _userRepo = new Mock<IRepository<User>>();
        _otpLoginRepo = new Mock<IRepository<OtpLogin>>();
        _repositoryFactory.Setup(x => x.Create<User>()).Returns(_userRepo.Object);
        _repositoryFactory.Setup(x => x.Create<OtpLogin>()).Returns(_otpLoginRepo.Object);
        _handler = new OtpRequestHandler(
            _mailer.Object,
            _otpGenerator.Object,
            _logger.Object,
            _repositoryFactory.Object,
            _dateTimeProvider.Object,
            _otpHasher.Object,
            _otpOptions,
            _managerOptions);
    }

    [TestCase("mundrayj@gmail.com", 1)]
    [TestCase("manager@test.com", 2)]
    public async Task Handle_CreatesNewUserAndSendsOtpSuccessfully(string email, int expectedUserTypeId)
    {
        var request = new OtpRequest { EmailAddress = email };
        _otpGenerator.Setup(x => x.GenerateToken()).Returns("OTP_TOKEN");
        _userRepo.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
            .ReturnsAsync([]);
        _otpHasher.Setup(x => x.Hash("OTP_TOKEN")).Returns(("HASH", "SALT"));
        _mailer.Setup(x => x.Send(request.EmailAddress, It.IsAny<object>())).ReturnsAsync(true);
        _userRepo.Setup(x => x.Create(It.IsAny<User>(), true)).Returns(Task.CompletedTask);
        _otpLoginRepo.Setup(x => x.Create(It.IsAny<OtpLogin>(), true)).Returns(Task.CompletedTask);
        _otpLoginRepo.Setup(x => x.Update(It.IsAny<OtpLogin>(), true)).Returns(Task.CompletedTask);

        var result = await _handler.Handle(request);

        result.Should().Match<Response>(r => r.Message == "Issued OTP successfully." && r.Success);
        _userRepo.Verify(x => x.Create(It.Is<User>(u => u.Email == request.EmailAddress && u.UserTypeId == expectedUserTypeId), true), Times.Once);
        _otpLoginRepo.Verify(x => x.Create(It.Is<OtpLogin>(o => o.CodeHash == "HASH" && o.HashSalt == "SALT" && o.User.Email == request.EmailAddress && o.ExpiryDate == _fixedTime.AddMinutes(5)), true), Times.Once);
        _otpLoginRepo.Verify(x => x.Update(It.Is<OtpLogin>(o => o.IssueDate == _fixedTime), true), Times.Once);
    }

    [Test]
    public async Task Handle_WhenUserExists_UsesExistingUser()
    {
        var existingUser = new User { Email = "mundrayj@gmail.com", UserTypeId = 2 };
        var request = new OtpRequest { EmailAddress = "mundrayj@gmail.com" };

        _otpGenerator.Setup(x => x.GenerateToken()).Returns("OTP_TOKEN");
        _userRepo.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
            .ReturnsAsync([existingUser]);
        _otpHasher.Setup(x => x.Hash("OTP_TOKEN")).Returns(("HASH", "SALT"));
        _mailer.Setup(x => x.Send(request.EmailAddress, It.IsAny<object>())).ReturnsAsync(true);
        _otpLoginRepo.Setup(x => x.Create(It.IsAny<OtpLogin>(), true)).Returns(Task.CompletedTask);
        _otpLoginRepo.Setup(x => x.Update(It.IsAny<OtpLogin>(), true)).Returns(Task.CompletedTask);

        var result = await _handler.Handle(request);

        result.Should().Match<Response>(r => r.Message == "Issued OTP successfully." && r.Success);
        _userRepo.Verify(x => x.Create(It.IsAny<User>(), true), Times.Never);
        _otpLoginRepo.Verify(x => x.Create(It.Is<OtpLogin>(o => o.User == existingUser), true), Times.Once);
        _otpLoginRepo.Verify(x => x.Update(It.IsAny<OtpLogin>(), true), Times.Once);
    }

    [Test]
    public async Task Handle_WhenEmailFails_ReturnsFalse()
    {
        var request = new OtpRequest { EmailAddress = "mundrayj@gmail.com" };

        _otpGenerator.Setup(x => x.GenerateToken()).Returns("OTP_TOKEN");
        _userRepo.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
            .ReturnsAsync([]);
        _otpHasher.Setup(x => x.Hash("OTP_TOKEN")).Returns(("HASH", "SALT"));
        _mailer.Setup(x => x.Send(request.EmailAddress, It.IsAny<object>())).ReturnsAsync(false);

        var result = await _handler.Handle(request);

        result.Should().Match<Response>(r => r.Message == "Unable to issue OTP. Email send failed." && !r.Success);
        _userRepo.Verify(x => x.Create(It.Is<User>(u => u.Email == request.EmailAddress), true), Times.Once);
        _otpLoginRepo.Verify(x => x.Create(It.IsAny<OtpLogin>(), true), Times.Once);
        _otpLoginRepo.Verify(x => x.Update(It.IsAny<OtpLogin>(), true), Times.Never);
    }
}
