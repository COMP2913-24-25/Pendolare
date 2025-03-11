using System.Text.Json;
using Identity.DataAccess.Models;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Identity.Util.ConfigHelpers;

/// <summary>
/// Loads configuration from the database and structures JSON values into hierarchical sections.
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

        foreach (var entry in context.Configuration.Where(cfg => cfg.Key.StartsWith(Constants.ConfigPrefix)))
        {
            var key = entry.Key[Constants.ConfigPrefix.Length..].TrimStart('.'); // Remove prefix
            SetValue(Data, key, entry.Value);
        }
    }

    private void SetValue(IDictionary<string, string?> data, string key, string value)
    {
        try
        {
            using var jsonDoc = JsonDocument.Parse(value);
            var root = jsonDoc.RootElement;

            if (root.ValueKind is JsonValueKind.Object)
            {
                foreach (var element in root.EnumerateObject())
                {
                    SetValue(data, $"{key}:{element.Name}", element.Value.ToString());
                }
                return;
            }
            
            if (root.ValueKind is JsonValueKind.Array)
            {
                int index = 0;
                foreach (var item in root.EnumerateArray())
                {
                    data[$"{key}:{index}"] = item.ToString();
                    index++;
                }
                return;
            }

            data[key] = root.ToString();
            return;
        }
        catch (JsonException)
        {
            // If not JSON, store it as a plain string
            data[key] = value;
        }
    }

}
