using FluentAssertions;
using Identity.DataAccess;
using Identity.DataAccess.Models;
using Microsoft.EntityFrameworkCore;
using Config = Identity.DataAccess.Models.Configuration;

namespace Identity.Tests.DataAccess
{
    [TestFixture]
    public class RepositoryTests
    {
        private PendoDatabaseContext _context;
        private Repository<Config> _repository;

        [SetUp]
        public void Setup()
        {
            var options = new DbContextOptionsBuilder<PendoDatabaseContext>()
                .UseInMemoryDatabase(databaseName: "TestDb_" + Guid.NewGuid())
                .Options;

            _context = new PendoDatabaseContext(options);
            _repository = new Repository<Config>(_context);
        }

        [TearDown]
        public async Task TearDown()
        {
            _context.Database.EnsureDeleted();
            await _context.DisposeAsync();
            await _repository.DisposeAsync();
        }

        [Test]
        public async Task Create_AddsNewEntity()
        {
            var entry = new Config { Key = "TestKey", Value = "TestValue" };

            await _repository.Create(entry);

            var savedEntry = await _context.Configuration.FirstOrDefaultAsync(e => e.Key == "TestKey");
            savedEntry.Should().NotBeNull();
            savedEntry.Value.Should().Be("TestValue");
        }

        [Test]
        public async Task Read_WithNullFilter_ReturnsAllEntities()
        {
            _context.Configuration.AddRange(Entries);
            await _context.SaveChangesAsync();

            var result = await _repository.Read();

            result.Should().HaveCount(2);
        }

        [Test]
        public async Task Read_Should_Return_Filtered_Entities()
        {
            _context.Configuration.AddRange(Entries);
            await _context.SaveChangesAsync();

            var result = await _repository.Read(e => e.Key == "Key1");

            result.Should().HaveCount(1);
            result.First().Value.Should().Be("Value1");
        }

        [Test]
        public async Task Update_ModifiesExistingEntity()
        {
            var entry = Entries.First();
            _context.Configuration.Add(entry);
            await _context.SaveChangesAsync();

            entry.Value = "NewValue";
            await _repository.Update(entry);

            _context.ChangeTracker.Clear();

            var updatedEntry = await _context.Configuration.FirstOrDefaultAsync(e => e.Key == "Key1");
            updatedEntry.Should().NotBeNull();
            updatedEntry.Value.Should().Be("NewValue");
        }

        [Test]
        public async Task Delete_RemovesExistingEntity()
        {
            var entry = Entries.First();
            _context.Configuration.Add(entry);
            await _context.SaveChangesAsync();

            await _repository.Delete(entry);
            _context.ChangeTracker.Clear();

            var deletedEntry = await _context.Configuration.FirstOrDefaultAsync(e => e.Key == "Key1");
            deletedEntry.Should().BeNull();
        }

        private static List<Config> Entries => [
                new Config { Key = "Key1", Value = "Value1" },
                new Config { Key = "Key2", Value = "Value2" }
                ];
    }
}