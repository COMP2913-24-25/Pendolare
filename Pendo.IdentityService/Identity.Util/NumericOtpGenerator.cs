using Identity.Configuration;
using Microsoft.Extensions.Options;
using System.Security.Cryptography;

namespace Identity.Util;

/// <inheritdoc/>
public class NumericOtpGenerator : IOtpGenerator
{
    private readonly OtpConfiguration _config;

    public NumericOtpGenerator(IOptions<OtpConfiguration> options)
    {
        _config = options.Value;
    }

    public string GenerateToken()
        => GetCode();

    private string GetCode()
    {
        var rng = RandomNumberGenerator.Create();
        var bytes = new byte[_config.OtpLength];
        rng.GetBytes(bytes);

        var code = new char[_config.OtpLength];
        for (int i = 0; i < bytes.Length; i++)
        {
            code[i] = (char)('0' + (bytes[i] % 10));
        }

        return new string(code);
    }
}
