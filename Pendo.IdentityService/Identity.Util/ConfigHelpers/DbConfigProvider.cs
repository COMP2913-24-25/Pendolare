using Identity.DataAccess;
using Identity.DataAccess.Models;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Identity.Util.ConfigHelpers;

/// <summary>
/// Loads configuration from database.
/// <see cref="https://learn.microsoft.com/en-us/dotnet/core/extensions/custom-configuration-provider"/> was used to help here!
/// </summary>
public class DbConfigProvider : ConfigurationProvider
{
    private readonly IServiceScopeFactory _scopeFactory;

    public DbConfigProvider(IServiceScopeFactory scopeFactory)
    {
        _scopeFactory = scopeFactory;
    }

    /// <inheritdoc/>
    public override void Load()
    {
        using var scope = _scopeFactory.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<PendoDatabaseContext>();

        Data = context.Configuration
            .Where(cfg => cfg.Key.StartsWith(Constants.ConfigPrefix))
            .ToDictionary(e => e.Key, e => (string?)e.Value);
    }
}
