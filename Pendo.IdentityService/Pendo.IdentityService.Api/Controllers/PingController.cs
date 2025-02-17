using Identity.Schema;
using Identity.Util;
using Microsoft.AspNetCore.Mvc;

namespace Pendo.IdentityService.Api.Controllers;

[ApiController]
[Route("api/ping")]
public class PingController : ControllerBase
{
    private readonly string[] _quotes = ["hello!", "go away", "yes i am working!", "bonjour!"];
    private readonly IDateTimeProvider _dateTimeProvider;

    public PingController(IDateTimeProvider dateTimeProvider)
    {
        _dateTimeProvider = dateTimeProvider;
    }

    [HttpGet(Name = "ping")]
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