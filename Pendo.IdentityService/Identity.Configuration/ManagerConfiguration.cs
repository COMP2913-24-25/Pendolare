namespace Identity.Configuration;

/// <summary>
/// Provides configuration for creation and administration of manager accounts.
/// </summary>
public class ManagerConfiguration
{
    public ManagerConfiguration() { }

    /// <summary>
    /// Provides a list of whitelisted emails that are able to create a manager account.
    /// </summary>
    public string[] Whitelist { get; set; } = Array.Empty<string>();
}