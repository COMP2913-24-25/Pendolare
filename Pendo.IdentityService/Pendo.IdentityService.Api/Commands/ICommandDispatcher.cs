using Identity.Schema;

namespace Pendo.IdentityService.Api.Commands;

/// <summary>
/// Dispatches commands to be executed.
/// </summary>
/// <remarks>
/// Inspiration for this pattern was found at <see cref="https://www.csharp.com/article/clean-architecture-and-command-pattern-in-asp-net-core-api-implementation/"/>
/// </remarks>
public interface ICommandDispatcher
{
    /// <summary>
    /// Dispatches a command of type <see cref="{TRequest}"/>.
    /// </summary>
    /// <typeparam name="TRequest">The type of request to process.</typeparam>
    /// <typeparam name="TResponse">The type of response to return.</typeparam>
    /// <returns>A response of type <see cref="{TResponse}"/></returns>
    Task<TResponse> Dispatch<TRequest, TResponse>(TRequest request)
        where TRequest : IRequest;
}