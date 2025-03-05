using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Identity.Util.ConfigHelpers;

/// <summary>
/// Implementation of <see cref="IConfigurationSource"/> to pull values from the Configuration table in the database.
/// </summary>
public class DbConfigSource : IConfigurationSource
{
    private readonly IServiceScopeFactory _serviceScopeFactory;

    public DbConfigSource(IServiceScopeFactory serviceScopeFactory)
    {
        _serviceScopeFactory = serviceScopeFactory;
    }

    public IConfigurationProvider Build(IConfigurationBuilder builder)
        => new DbConfigProvider(_serviceScopeFactory);
}
