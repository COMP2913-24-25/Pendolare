using Identity.Schema;
using Identity.Util;
using Microsoft.AspNetCore.Mvc;

namespace Pendo.IdentityService.Api.Controllers;

[ApiController]
[Route("api/Identity/Ping")]
[Consumes(Constants.AppJson)]
[Produces(Constants.AppJson)]
public class PingController : ControllerBase
{
    private readonly string[] _quotes = ["hello!", "go away", "yes i am working!", "bonjour!"];
    private readonly IDateTimeProvider _dateTimeProvider;

    public PingController(IDateTimeProvider dateTimeProvider)
    {
        _dateTimeProvider = dateTimeProvider;
    }

    [HttpGet(Name = "Ping")]
    public PingResponse Ping()
    {
        var rng = new Random();
        return new PingResponse
        {
            Message = _quotes[rng.Next(0, _quotes.Length)],
            TimeSent = _dateTimeProvider.UtcNow()
        };
    }
}