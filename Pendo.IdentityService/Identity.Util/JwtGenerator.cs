using Identity.Configuration;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.JsonWebTokens;
using Microsoft.IdentityModel.Tokens;
using System.Security.Claims;
using System.Text;

namespace Identity.Util;

/// <inheritdoc/>
public class JwtGenerator : IJwtGenerator
{
    private readonly JwtConfiguration _config;
    private readonly IDateTimeProvider _dateTimeProvider;

    public JwtGenerator(IOptions<JwtConfiguration> options, IDateTimeProvider dateTimeProvider)
    {
        _config = options.Value;
        _dateTimeProvider = dateTimeProvider;
    }

    public string GenerateJwt(string userEmail, bool isManager)
    {
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_config.SecretKey));
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var tokenDescriptor = new SecurityTokenDescriptor
        {
            Issuer = _config.Issuer,
            Audience = isManager ? _config.ManagerAudience : _config.AppAudience,
            Claims = GetClaims(userEmail, isManager),
            Expires = _dateTimeProvider.UtcNow().AddMinutes(_config.ExpiresInMinutes),
            SigningCredentials = credentials
        };

        var handler = new JsonWebTokenHandler();
        return handler.CreateToken(tokenDescriptor);
    }

    private Dictionary<string, object> GetClaims(string userEmail, bool isManager) 
        => new()
        {
                { ClaimTypes.Name, userEmail },
                { Constants.UserTypeClaim, isManager ? Constants.Manager : Constants.User },
                { JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString() }
            };
}