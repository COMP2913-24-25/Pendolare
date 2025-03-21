using Azure.Core;
using Identity.Schema;
using Identity.Schema.User;
using Identity.Util;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using Pendo.IdentityService.Api.Commands;
using Swashbuckle.AspNetCore.Annotations;

namespace Pendo.IdentityService.Api.Controllers;

[Route("api/Identity")]
[ApiController]
[Consumes(Constants.AppJson)]
[Produces(Constants.AppJson)]
public class UserController : ControllerBase
{
    private readonly ICommandDispatcher _commandDispatcher;
    private readonly ILogger<UserController> _logger;

    public UserController(ICommandDispatcher commandDispatcher, ILogger<UserController> logger)
    {
        _commandDispatcher = commandDispatcher;
        _logger = logger;
    }

    [HttpPatch("UpdateUser", Name = "Update User")]
    [SwaggerResponse(200, type: typeof(Response))]
    [SwaggerResponse(400, type: typeof(Response))]
    public async Task<IActionResult> UpdateUser([FromBody] UpdateUserRequest request)
    {
        _logger.LogDebug($"Executing {nameof(UpdateUserRequest)}. Body: {JsonConvert.SerializeObject(request)}");

        var result = await _commandDispatcher.Dispatch<UpdateUserRequest, Response>(request);

        return result.Success ? Ok(result) : BadRequest(result);
    }

    [HttpPost("GetUser", Name = "Get User")]
    [SwaggerResponse(200, type: typeof(GetUserResponse))]
    [SwaggerResponse(400, type: typeof(GetUserResponse))]
    public async Task<IActionResult> GetUser([FromBody] GetUserRequest request)
    {
        _logger.LogDebug($"Executing {nameof(GetUserRequest)}. Body: {JsonConvert.SerializeObject(request)}");

        var result = await _commandDispatcher.Dispatch<GetUserRequest, GetUserResponse>(request);

        return result.Success ? Ok(result) : BadRequest(result);
    }
}