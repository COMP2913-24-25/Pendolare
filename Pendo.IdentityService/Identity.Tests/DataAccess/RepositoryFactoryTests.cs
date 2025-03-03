using FluentAssertions;
using Identity.DataAccess;
using Identity.DataAccess.Models;
using Microsoft.EntityFrameworkCore;
using Moq;

namespace Identity.Tests.DataAccess;

public class RepositoryFactoryTests
{
    private IRepositoryFactory _repositoryFactory;

    [SetUp]
    public void Setup()
    {
        var opt = new DbContextOptionsBuilder<PendoDatabaseContext>()
            .UseInMemoryDatabase("testDB").Options;

        var ctx = new PendoDatabaseContext(opt);
        var provider = new Mock<IServiceProvider>();

        provider.Setup(p => p.GetService(typeof(PendoDatabaseContext))).Returns(ctx);

        _repositoryFactory = new RepositoryFactory(provider.Object);
    }

    [Test]
    public void Create_ReturnsModelOfCorrectType() 
        => _repositoryFactory.Create<Identity.DataAccess.Models.Configuration>()
            .Should().NotBeNull().And
            .BeAssignableTo<IRepository<Identity.DataAccess.Models.Configuration>>();
}
