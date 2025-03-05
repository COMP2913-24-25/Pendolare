namespace Identity.Util;

public interface IOtpGenerator
{
    /// <summary>
    /// Generates a new OTP.
    /// </summary>
    string GenerateToken();
}
