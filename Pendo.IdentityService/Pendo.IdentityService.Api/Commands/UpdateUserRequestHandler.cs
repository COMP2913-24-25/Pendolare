using Identity.DataAccess;
using Identity.DataAccess.Models;
using Identity.Schema;
using Identity.Schema.User;

namespace Pendo.IdentityService.Api.Commands;

/// <inheritdoc/>
public class UpdateUserRequestHandler : ICommandHandler<UpdateUserRequest, Response>
{
    private readonly IRepositoryFactory _repositoryFactory;
    private readonly ILogger<UpdateUserRequestHandler> _logger;

    public UpdateUserRequestHandler(IRepositoryFactory repositoryFactory, ILogger<UpdateUserRequestHandler> logger)
    {
        _repositoryFactory = repositoryFactory;
        _logger = logger;
    }

    public async Task<Response> Handle(UpdateUserRequest request)
    {
        await using var repo = _repositoryFactory.Create<User>();

        var user = (await repo.Read(u => u.UserId == request.UserId)).FirstOrDefault();

        if (user is null)
        {
            _logger.LogError($"Unable to update user {request.UserId}. User not found.");
            return Response.FailureResponse("Unable to update user. User not found.");
        }

        if (request.FirstName is not null or "")
            user.FirstName = request.FirstName;

        if (request.LastName is not null or "")
            user.LastName = request.LastName;

        var msg = "Successfully updated user.";
        await repo.Update(user);
        _logger.LogDebug($"{msg} UserId: {request.UserId}");

        return Response.SuccessResponse(msg);
    }
}
