using Identity.DataAccess;
using Identity.DataAccess.Models;
using Identity.Schema.User.Auth;
using Identity.Util;

namespace Pendo.IdentityService.Api.Commands;

public class VerifyOtpRequestHandler : ICommandHandler<VerifyOtpRequest, VerifyOtpResponse>
{
    private readonly IJwtGenerator _jwtGenerator;
    private readonly IRepositoryFactory _repositoryFactory;

    public VerifyOtpRequestHandler(IJwtGenerator jwtGenerator, IRepositoryFactory repositoryFactory)
    {
        _jwtGenerator = jwtGenerator;
        _repositoryFactory = repositoryFactory;
    }

    public async Task<VerifyOtpResponse> Handle(VerifyOtpRequest request)
    {
        await using var repo = _repositoryFactory.Create<OtpLogin>();

        var hashedCode = request.Otp; //TODO : ADD HASHING

        var codeResult = (await repo.Read(login => login.CodeHash == hashedCode)).FirstOrDefault();

        if (codeResult is null)
            return new VerifyOtpResponse { 
                Jwt = "", 
                Authenticated = false 
            };

        codeResult.Verified = true;
        await repo.Update(codeResult);

        var isNewUser = (await repo.Read(login => login.UserId == codeResult.UserId && login.Verified)).Count() > 1;

        await using var userRepo = _repositoryFactory.Create<User>();
        var user = (await userRepo.Read(us => us.UserId == codeResult.UserId)).First();

        return new VerifyOtpResponse
        {
            Jwt = _jwtGenerator.GenerateJwt(user.Email, user.UserTypeId == 2),
            IsNewUser = isNewUser,
            Authenticated = true
        };
    }
}
