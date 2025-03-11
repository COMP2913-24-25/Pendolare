using Identity.Schema;
using Identity.Schema.User;
using Identity.Util;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using Pendo.IdentityService.Api.Commands;
using Swashbuckle.AspNetCore.Annotations;

namespace Pendo.IdentityService.Api.Controllers;

[Route("api/Identity/UpdateUser")]
[ApiController]
[Consumes(Constants.AppJson)]
[Produces(Constants.AppJson)]
public class UpdateUserController : ControllerBase
{
    private readonly ICommandDispatcher _commandDispatcher;
    private readonly ILogger<UpdateUserController> _logger;

    public UpdateUserController(ICommandDispatcher commandDispatcher, ILogger<UpdateUserController> logger)
    {
        _commandDispatcher = commandDispatcher;
        _logger = logger;
    }

    [HttpPatch(Name = "Update User")]
    [SwaggerResponse(200, type: typeof(Response))]
    [SwaggerResponse(400, type: typeof(Response))]
    public async Task<IActionResult> UpdateUser([FromBody] UpdateUserRequest request)
    {
        _logger.LogDebug($"Executing {nameof(UpdateUserRequest)}. Body: {JsonConvert.SerializeObject(request)}");

        var result = await _commandDispatcher.Dispatch<UpdateUserRequest, Response>(request);

        return result.Success ? Ok(result) : BadRequest(result);
    }

}