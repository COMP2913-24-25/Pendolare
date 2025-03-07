using Identity.Schema.User.Auth;
using Microsoft.AspNetCore.Mvc;
using Pendo.IdentityService.Api.Commands;
using Newtonsoft.Json;
using Identity.Schema;
using Identity.Util;
using Swashbuckle.AspNetCore.Annotations;

namespace Pendo.IdentityService.Api.Controllers;

[Route("api/Identity")]
[ApiController]
[Consumes(Constants.AppJson)]
[Produces(Constants.AppJson)]
public class AuthController : ControllerBase
{
    private readonly ICommandDispatcher _commandDispatcher;
    private readonly ILogger _logger;

    public AuthController(ICommandDispatcher commandDispatcher, ILogger<AuthController> logger)
    {
        _commandDispatcher = commandDispatcher;
        _logger = logger;
    }

    [HttpPost("RequestOtp", Name = "Request One-Time-Passcode Email")]
    [SwaggerResponse(200, type: typeof(Response))]
    [SwaggerResponse(400, type: typeof(Response))]
    public async Task<IActionResult> RequestOtp([FromBody] OtpRequest request)
    {
        _logger.LogDebug($"Executing {nameof(OtpRequest)}. Body: {JsonConvert.SerializeObject(request)}");
        var result = await _commandDispatcher.Dispatch<OtpRequest, Response>(request);

        return result.Success ? Ok(result) : BadRequest(result);
    }

    [HttpPost("VerifyOtp", Name = "Verify One-Time-Passcode")]
    [SwaggerResponse(200, type: typeof(VerifyOtpResponse))]
    [SwaggerResponse(400, type: typeof(VerifyOtpResponse))]
    public async Task<IActionResult> VerifyOtp([FromBody] VerifyOtpRequest request)
    {
        _logger.LogDebug($"Executing {nameof(VerifyOtpRequest)}. Body: {JsonConvert.SerializeObject(request)}");
        var result = await _commandDispatcher.Dispatch<VerifyOtpRequest, VerifyOtpResponse>(request);

        return result.Authenticated ? Ok(result) : BadRequest(result);
    }
}