using Identity.Schema;

namespace Pendo.IdentityService.Api.Commands;

/// <summary>
/// Handles requests of type <see cref="{TRequest}"/>, returning a <see cref="{TResponse}"/>.
/// </summary>
/// <typeparam name="TRequest">The type of request to process.</typeparam>
/// <typeparam name="TResponse">The type of response to process.</typeparam>
public interface ICommandHandler<TRequest, TResponse> 
    where TRequest : IRequest 
{
    /// <summary>
    /// Handles the request, returning a response object.
    /// </summary>
    Task<TResponse> Handle(TRequest request);
}
