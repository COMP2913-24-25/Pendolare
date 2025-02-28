using Identity.Configuration;
using Identity.Schema.User.Auth;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Pendo.IdentityService.Api.Commands;
using Newtonsoft.Json;

namespace Pendo.IdentityService.Api.Controllers;

[Route("api/auth")]
[ApiController]
public class AuthController : ControllerBase
{
    private readonly ICommandDispatcher _commandDispatcher;
    private readonly ILogger _logger;

    public AuthController(ICommandDispatcher commandDispatcher, ILogger<AuthController> logger)
    {
        _commandDispatcher = commandDispatcher;
        _logger = logger;
    }

    [HttpPost("request-otp", Name = "Request One-Time-Passcode Email")]
    public async Task<IActionResult> RequestOtp([FromBody] OtpRequest request)
    {
        _logger.LogDebug($"Executing {nameof(OtpRequest)}. Body: {JsonConvert.SerializeObject(request)}");
        var result = await _commandDispatcher.Dispatch<OtpRequest, bool>(request);

        return result ? Ok() : BadRequest();
    }

    [HttpPost("verify-otp", Name = "Verify One-Time-Passcode")]
    public async Task<IActionResult> VerifyOtp([FromBody] VerifyOtpRequest request)
    {
        _logger.LogDebug($"Executing {nameof(VerifyOtpRequest)}. Body: {JsonConvert.SerializeObject(request)}");
        var result = await _commandDispatcher.Dispatch<VerifyOtpRequest, VerifyOtpResponse>(request);

        return result.Authenticated ? Ok(result) : BadRequest(result);
    }
}