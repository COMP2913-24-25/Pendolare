
using Identity.Schema;

namespace Pendo.IdentityService.Api.Commands;

public class CommandDispatcher : ICommandDispatcher
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<CommandDispatcher> _logger;

    public CommandDispatcher(IServiceProvider serviceProvider, ILogger<CommandDispatcher> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    public async Task<TResponse> Dispatch<TRequest, TResponse>(TRequest request) 
        where TRequest : IRequest
    {
        _logger.LogInformation($"Dispatching {typeof(TRequest).Name} to handler.");

        var handler = _serviceProvider.GetRequiredService<ICommandHandler<TRequest, TResponse>>();
        var response = await handler.Handle(request);

        _logger.LogInformation($"Finished handling {typeof(TRequest).Name}");
        return response;
    }
}
