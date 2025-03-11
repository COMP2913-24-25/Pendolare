namespace Identity.Util;

public interface IOtpHasher
{
    /// <summary>
    /// Hashes an OTP code.
    /// </summary>
    /// <param name="otp">The code to hash.</param>
    /// <returns>The resulting hash, along with the salt used.</returns>
    (string hash, string salt) Hash(string otp);

    /// <summary>
    /// Verifies a hash with the given salt.
    /// </summary>
    bool VerifyHash(string otp, string hash, string salt);
}
