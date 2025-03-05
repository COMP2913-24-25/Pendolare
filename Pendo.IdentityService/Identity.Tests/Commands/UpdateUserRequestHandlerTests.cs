using System.Linq.Expressions;
using FluentAssertions;
using Identity.DataAccess;
using Identity.DataAccess.Models;
using Identity.Schema.User;
using Microsoft.Extensions.Logging;
using Moq;
using Pendo.IdentityService.Api.Commands;

namespace Identity.Tests.Commands;

[TestFixture]
public class UpdateUserRequestHandlerTests
{
    private Mock<IRepositoryFactory> _repositoryFactory;
    private Mock<IRepository<User>> _userRepository;
    private Mock<ILogger<UpdateUserRequestHandler>> _logger;
    private UpdateUserRequestHandler _handler;

    [SetUp]
    public void Setup()
    {
        _repositoryFactory = new Mock<IRepositoryFactory>();
        _userRepository = new Mock<IRepository<User>>();
        _logger = new Mock<ILogger<UpdateUserRequestHandler>>();

        _repositoryFactory.Setup(x => x.Create<User>())
            .Returns(_userRepository.Object);

        _handler = new UpdateUserRequestHandler(_repositoryFactory.Object, _logger.Object);
    }

    [Test]
    public async Task Handle_UserNotFound_ReturnsFailureResponse()
    {
        var request = new UpdateUserRequest { UserId = Guid.NewGuid(), FirstName = "New", LastName = "Name" };
        _userRepository.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
            .ReturnsAsync(new List<User>());

        var result = await _handler.Handle(request);

        result.Success.Should().BeFalse();
        result.Message.Should().Be("Unable to update user. User not found.");
        _userRepository.Verify(x => x.Update(It.IsAny<User>(), true), Times.Never);
        _logger.Verify(x => x.Log(
            LogLevel.Error,
            It.IsAny<EventId>(),
            It.Is<It.IsAnyType>((v, t) => v.ToString().Contains(request.UserId.ToString())),
            null,
            It.IsAny<Func<It.IsAnyType, Exception?, string>>()), Times.Once);
    }

    [Test]
    public async Task Handle_UserFound_UpdatesFirstAndLastNameSuccessfully()
    {
        var userId = Guid.NewGuid();
        var existingUser = new User { UserId = userId, FirstName = "OldFirst", LastName = "OldLast" };
        var request = new UpdateUserRequest { UserId = userId, FirstName = "NewFirst", LastName = "NewLast" };

        _userRepository.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
            .ReturnsAsync(new List<User> { existingUser });
        _userRepository.Setup(x => x.Update(It.IsAny<User>(), true))
            .Returns(Task.CompletedTask);

        var result = await _handler.Handle(request);

        result.Success.Should().BeTrue();
        result.Message.Should().Be("Successfully updated user.");
        existingUser.FirstName.Should().Be("NewFirst");
        existingUser.LastName.Should().Be("NewLast");
        _userRepository.Verify(x => x.Update(It.Is<User>(u =>
            u.UserId == request.UserId &&
            u.FirstName == "NewFirst" &&
            u.LastName == "NewLast"), true), Times.Once);
        _logger.Verify(x => x.Log(
            LogLevel.Debug,
            It.IsAny<EventId>(),
            It.Is<It.IsAnyType>((v, t) => v.ToString().Contains($"Successfully updated user. UserId: {request.UserId}")),
            null,
            It.IsAny<Func<It.IsAnyType, Exception?, string>>()), Times.Once);
    }

    [Test]
    public async Task Handle_UserFound_UpdateOnlyNonEmptyValues()
    {
        var userId = Guid.NewGuid();
        var existingUser = new User { UserId = userId, FirstName = "ExistingFirst", LastName = "ExistingLast" };
        var request = new UpdateUserRequest { UserId = userId, FirstName = "UpdatedFirst", LastName = "" };

        _userRepository.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
            .ReturnsAsync(new List<User> { existingUser });
        _userRepository.Setup(x => x.Update(It.IsAny<User>(), true))
            .Returns(Task.CompletedTask);

        var result = await _handler.Handle(request);

        result.Success.Should().BeTrue();
        result.Message.Should().Be("Successfully updated user.");
        existingUser.FirstName.Should().Be("UpdatedFirst");
        existingUser.LastName.Should().Be("");
        _userRepository.Verify(x => x.Update(It.Is<User>(u =>
            u.UserId == request.UserId &&
            u.FirstName == "UpdatedFirst" &&
            u.LastName == ""), true), Times.Once);
        _logger.Verify(x => x.Log(
            LogLevel.Debug,
            It.IsAny<EventId>(),
            It.Is<It.IsAnyType>((v, t) => v.ToString().Contains($"Successfully updated user. UserId: {request.UserId}")),
            null,
            It.IsAny<Func<It.IsAnyType, Exception?, string>>()), Times.Once);
    }
}