using Identity.DataAccess;
using Identity.DataAccess.Models;
using Identity.Schema.User.Auth;
using Identity.Util;

namespace Pendo.IdentityService.Api.Commands;


/// <inheritdoc/>
public class VerifyOtpRequestHandler : ICommandHandler<VerifyOtpRequest, VerifyOtpResponse>
{
    private readonly IJwtGenerator _jwtGenerator;
    private readonly IRepositoryFactory _repositoryFactory;
    private readonly IDateTimeProvider _dateTimeProvider;
    private readonly IOtpHasher _otpHasher;
    private readonly ILogger _logger;

    public VerifyOtpRequestHandler(
        IJwtGenerator jwtGenerator, 
        IRepositoryFactory repositoryFactory, 
        ILogger<VerifyOtpRequestHandler> logger, 
        IDateTimeProvider dateTimeProvider,
        IOtpHasher otpHasher)
    {
        _jwtGenerator = jwtGenerator;
        _repositoryFactory = repositoryFactory;
        _dateTimeProvider = dateTimeProvider;
        _otpHasher = otpHasher;
        _logger = logger;
    }

    /// <summary>
    /// Handles <see cref="VerifyOtpRequest"/>.
    /// </summary>
    /// <param name="request"></param>
    /// <returns></returns>
    public async Task<VerifyOtpResponse> Handle(VerifyOtpRequest request)
    {
        await using var userRepo = _repositoryFactory.Create<User>();

        var userResult = await userRepo.Read(user => user.Email.ToLower() == request.EmailAddress.ToLower());

        if (userResult is null || userResult.Count() is > 1 or 0)
        {
            var msg = "User with the given email address either does not exist or the unique constraint has been violated. Please check logs and database records.";
            _logger.LogWarning(msg);

            return new VerifyOtpResponse
            {
                Jwt = "",
                Authenticated = false,
                Success = false,
                Message = msg
            };
        }

        var user = userResult.First();

        await using var repo = _repositoryFactory.Create<OtpLogin>();

        var codeResult = (await repo.Read(login => login.UserId == user.UserId))
            .OrderByDescending(login => login.IssueDate)
            .FirstOrDefault();

        if (codeResult is null)
            return new VerifyOtpResponse
            {
                Jwt = "",
                Authenticated = false
            };

        if (codeResult.ExpiryDate < _dateTimeProvider.UtcNow())
        {
            var msg = "Cannot log user in. Otp has expired.";
            _logger.LogWarning(msg);
            return new VerifyOtpResponse
            {
                Jwt = "",
                Authenticated = false,
                Success = false,
                Message = msg
            };
        }

        if (!_otpHasher.VerifyHash(request.Otp, codeResult.CodeHash, codeResult.HashSalt))
        {
            var msg = "Cannot log user in. Otp is invalid.";
            _logger.LogWarning(msg);
            return new VerifyOtpResponse
            {
                Jwt = "",
                Authenticated = false,
                Success = false,
                Message = msg
            };
        }

        codeResult.Verified = true;
        await repo.Update(codeResult);

        // Should probably do this more robustly, ok for now.
        var isNewUser = (await repo.Read(login => login.UserId == codeResult.UserId && login.Verified))?.Count() is 1;

        return new VerifyOtpResponse
        {
            Jwt = _jwtGenerator.GenerateJwt(user.Email, user.UserTypeId is 2),
            IsNewUser = isNewUser,
            Authenticated = true
        };
    }
}
