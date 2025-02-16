using Microsoft.AspNetCore.Cryptography.KeyDerivation;
using System.Security.Cryptography;
using System.Text;

namespace Identity.Util;

/// <inheritdoc/>
public class OtpHasher : IOtpHasher
{
    public (string hash, string salt) Hash(string otp)
    {
        var salt = RandomNumberGenerator.GetBytes(16);
        return (Hash(otp, salt), Convert.ToBase64String(salt));
    }

    public bool VerifyHash(string otp, string hash, string salt)
        => hash == Hash(otp, Convert.FromBase64String(salt));

    private static string Hash(string otp, byte[] salt) 
        => Convert.ToBase64String(KeyDerivation.Pbkdf2(otp, salt, KeyDerivationPrf.HMACSHA256, 10000, 32));
}
