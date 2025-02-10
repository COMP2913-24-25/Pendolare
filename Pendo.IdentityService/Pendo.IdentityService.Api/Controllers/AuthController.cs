using Identity.Configuration;
using Identity.Schema.User.Auth;
using Identity.Util;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;

namespace Pendo.IdentityService.Api.Controllers;

[Route("api/auth")]
[ApiController]
public class AuthController : ControllerBase
{
    private readonly IMailer _mailer;
    private readonly IOtpGenerator _otpGenerator;
    private readonly IJwtGenerator _jwtGenerator;

    public AuthController(IMailer mailer, IOtpGenerator otpGenerator, IJwtGenerator jwtGenerator)
    {
        _mailer = mailer;
        _otpGenerator = otpGenerator;
        _jwtGenerator = jwtGenerator;
    }

    [HttpPost("request-otp", Name = "Request One-Time-Passcode Email")]
    public async Task<IActionResult> RequestOtp([FromBody] OtpRequest request)
    {
        var otp = _otpGenerator.GenerateToken();
        //Persist OTP to table

        var result = await _mailer.Send(request.EmailAddress, new
        {
            otp_code = otp
        });

        //Record as sent if success, if not, record as failed

        return result ? Ok() : BadRequest();
    }


    [HttpPost("verify-otp", Name = "Verify One-Time-Passcode")]
    public IActionResult VerifyOtp([FromBody] VerifyOtpRequest request)
    {
        //verify otp against the one we popped in the database
        if (request.Otp == "123456")
        {
            //Record login as allowed
        }

        //Issue JWT if valid!
        return Ok(new VerifyOtpResponse
        { 
            Jwt = _jwtGenerator.GenerateJwt("email@email.net", false) 
        });
    }
}