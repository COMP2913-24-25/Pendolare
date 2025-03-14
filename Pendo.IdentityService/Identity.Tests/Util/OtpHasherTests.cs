using FluentAssertions;
using Identity.Util;

namespace Identity.Tests.Util;

[TestFixture]
public class OtpHasherTests
{
    private OtpHasher _otpHasher;

    [SetUp]
    public void Setup()
    {
        _otpHasher = new OtpHasher();
    }

    [Test]
    public void Hash_ShouldReturnValidHashAndSalt()
    {
        string otp = "123456";

        var (hash, salt) = _otpHasher.Hash(otp);

        hash.Should().NotBeNullOrEmpty();
        salt.Should().NotBeNullOrEmpty();
    }

    [Test]
    public void VerifyHash_WithCorrectOtp_ReturnsTrue()
    {
        string otp = "123456";
        var (hash, salt) = _otpHasher.Hash(otp);

        _otpHasher.VerifyHash(otp, hash, salt).Should().BeTrue();
    }

    [Test]
    public void VerifyHash_WithIncorrectOtp_ReturnsFalse()
    {
        var (hash, salt) = _otpHasher.Hash("123456");
        
        _otpHasher.VerifyHash("654321", hash, salt).Should().BeFalse();
    }

    [Test]
    public void VerifyHash_WithModifiedHash_ReturnsFalse()
    {
        string otp = "123456";
        var (hash, salt) = _otpHasher.Hash(otp);
        string modifiedHash = hash.Substring(0, hash.Length - 2) + "XX";

        _otpHasher.VerifyHash(otp, modifiedHash, salt).Should().BeFalse();
    }

    [Test]
    public void VerifyHash_WithModifiedSalt_ReturnsFalse()
    {
        string otp = "123456";
        var (hash, salt) = _otpHasher.Hash(otp);
        string modifiedSalt = salt.Substring(0, salt.Length - 2) + "XX";

        _otpHasher.VerifyHash(otp, hash, modifiedSalt).Should().BeFalse();
    }
}