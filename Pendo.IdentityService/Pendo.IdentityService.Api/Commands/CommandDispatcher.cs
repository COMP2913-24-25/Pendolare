
using Identity.Schema;

namespace Pendo.IdentityService.Api.Commands;

public class CommandDispatcher : ICommandDispatcher
{
    private readonly IServiceProvider _serviceProvider;

    public CommandDispatcher(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public async Task<TResponse> Dispatch<TRequest, TResponse>(TRequest request) 
        where TRequest : IRequest
    {
        var handler = _serviceProvider.GetRequiredService<ICommandHandler<TRequest, TResponse>>();
        return await handler.Handle(request);
    }
}
