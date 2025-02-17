using Identity.Schema;

namespace Pendo.IdentityService.Api.Commands;

public interface ICommandHandler<TRequest, TResponse> 
    where TRequest : IRequest 
{
    Task<TResponse> Handle(TRequest request);
}
