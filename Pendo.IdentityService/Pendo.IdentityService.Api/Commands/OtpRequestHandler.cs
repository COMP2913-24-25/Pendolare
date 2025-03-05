using Identity.Configuration;
using Identity.DataAccess;
using Identity.DataAccess.Models;
using Identity.Schema;
using Identity.Schema.User.Auth;
using Identity.Util;
using Microsoft.Extensions.Options;

namespace Pendo.IdentityService.Api.Commands;

/// <inheritdoc/>
public class OtpRequestHandler : ICommandHandler<OtpRequest, Response>
{
    private readonly IMailer _mailer;
    private readonly IOtpGenerator _otpGenerator;
    private readonly IRepositoryFactory _repositoryFactory;
    private readonly IDateTimeProvider _dateTimeProvider;
    private readonly IOtpHasher _otpHasher;
    private readonly ILogger _logger;

    private readonly OtpConfiguration _otpConfig;
    private readonly ManagerConfiguration _managerConfig;

    public OtpRequestHandler(
        IMailer mailer, 
        IOtpGenerator otpGenerator,
        ILogger<OtpRequestHandler> logger,
        IRepositoryFactory repositoryFactory,
        IDateTimeProvider dateTimeProvider,
        IOtpHasher otpHasher,
        IOptions<OtpConfiguration> otpOptions,
        IOptions<ManagerConfiguration> managerOptions)
    {
        _mailer = mailer;
        _otpGenerator = otpGenerator;
        _repositoryFactory = repositoryFactory;
        _dateTimeProvider = dateTimeProvider;
        _otpHasher = otpHasher;
        _logger = logger;
        _otpConfig = otpOptions.Value;
        _managerConfig = managerOptions.Value;
    }

    public async Task<Response> Handle(OtpRequest request)
    {
        var token = _otpGenerator.GenerateToken();
        await using var userRepo = _repositoryFactory.Create<User>();

        //Find user with email
        var user = (await userRepo.Read(user => user.Email == request.EmailAddress))?.FirstOrDefault();

        if (user is null)
        {
            _logger.LogInformation($"No user found for email '{request.EmailAddress}'. Creating a new user.");
            var userTypeId = 1; //Standard User

            if (_managerConfig.Whitelist.Contains(request.EmailAddress.ToLower()))
            {
                _logger.LogInformation($"Email {request.EmailAddress} is in manager whitelist. Creating account as manager.");
                userTypeId = 2; //Manager
            }

            user = new User
            {
                Email = request.EmailAddress,
                UserTypeId = userTypeId //These IDs should NOT change at any point.
            };

            await userRepo.Create(user);
        }

        (var codeHash, var codeSalt) = _otpHasher.Hash(token);

        var login = new OtpLogin
        {
            CodeHash = codeHash,
            HashSalt = codeSalt,
            User = user,
            ExpiryDate = _dateTimeProvider.UtcNow().AddMinutes(_otpConfig.ValidMinutes)
        };

        await using var otpLoginRepo = _repositoryFactory.Create<OtpLogin>();
        await otpLoginRepo.Create(login);

        var result = await SendEmail(request.EmailAddress, token);

        if (!result)
        {
            var msg = "Unable to issue OTP. Email send failed.";
            _logger.LogError(msg);
            return Response.FailureResponse(msg);
        }

        login.IssueDate = _dateTimeProvider.UtcNow(); //Set as issued.
        await otpLoginRepo.Update(login);
        return Response.SuccessResponse("Issued OTP successfully.");
    }

    private async Task<bool> SendEmail(string email, string otp) 
        => await _mailer.Send(email, new
        {
            otp_code = otp
        });
}
