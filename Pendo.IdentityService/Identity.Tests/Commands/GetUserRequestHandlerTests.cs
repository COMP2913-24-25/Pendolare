using System.Linq.Expressions;
using FluentAssertions;
using Identity.DataAccess;
using Identity.DataAccess.Models;
using Identity.Schema.User;
using Microsoft.Extensions.Logging;
using Moq;
using Pendo.IdentityService.Api.Commands;

namespace Identity.Tests.Commands
{
    [TestFixture]
    public class GetUserRequestHandlerTests
    {
        private Mock<IRepositoryFactory> _repositoryFactory;
        private Mock<IRepository<User>> _userRepository;
        private Mock<ILogger<GetUserRequestHandler>> _logger;
        private GetUserRequestHandler _handler;

        [SetUp]
        public void Setup()
        {
            _repositoryFactory = new Mock<IRepositoryFactory>();
            _userRepository = new Mock<IRepository<User>>();
            _logger = new Mock<ILogger<GetUserRequestHandler>>();

            _repositoryFactory.Setup(x => x.Create<User>())
                .Returns(_userRepository.Object);

            _handler = new GetUserRequestHandler(_repositoryFactory.Object, _logger.Object);
        }

        [Test]
        public async Task Handle_UserNotFound_ReturnsFailureResponse()
        {
            var request = new GetUserRequest { UserId = Guid.NewGuid() };
            _userRepository.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
                .ReturnsAsync(new List<User>());

            var result = await _handler.Handle(request);

            result.Success.Should().BeFalse();
            result.Message.Should().Be("No user could be found.");
            _logger.Verify(x => x.Log(
                LogLevel.Error,
                It.IsAny<EventId>(),
                It.Is<It.IsAnyType>((v, t) => v.ToString().Contains(request.UserId.ToString())),
                null,
                It.IsAny<Func<It.IsAnyType, Exception?, string>>()), Times.Once);
        }

        [Test]
        public async Task Handle_UserFound_ReturnsUserDetailsSuccessfully()
        {
            var userId = Guid.NewGuid();
            var user = new User { UserId = userId, FirstName = "John", LastName = "Doe", UserRating = 4.5 };
            var request = new GetUserRequest { UserId = userId };

            _userRepository.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
                .ReturnsAsync(new List<User> { user });

            var result = await _handler.Handle(request);

            result.Success.Should().BeTrue();
            result.Message.Should().Be("");
            result.FirstName.Should().Be("John");
            result.LastName.Should().Be("Doe");
            result.UserRating.Should().Be(4.5);
        }

        [Test]
        public async Task Handle_UserFound_NullNames_DefaultsToEmptyString()
        {
            var userId = Guid.NewGuid();
            var user = new User { UserId = userId, FirstName = null, LastName = null, UserRating = 3.8 };
            var request = new GetUserRequest { UserId = userId };

            _userRepository.Setup(x => x.Read(It.IsAny<Expression<Func<User, bool>>>()))
                .ReturnsAsync(new List<User> { user });

            var result = await _handler.Handle(request);

            result.Success.Should().BeTrue();
            result.Message.Should().Be("");
            result.FirstName.Should().Be("");
            result.LastName.Should().Be("");
            result.UserRating.Should().Be(3.8);
        }
    }
}