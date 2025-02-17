using Microsoft.Extensions.Options;

namespace Identity.Tests;

internal class SimpleOptions<TOptions> : IOptions<TOptions> where TOptions : class
{
    private readonly TOptions _value;

    internal SimpleOptions(TOptions value)
        => _value = value;

    public TOptions Value => _value;
}
