using Identity.DataAccess;
using Identity.DataAccess.Models;
using Identity.Schema.User;

namespace Pendo.IdentityService.Api.Commands;

/// <inheritdoc/>
public class GetUserRequestHandler : ICommandHandler<GetUserRequest, GetUserResponse>
{
    private readonly IRepositoryFactory _repositoryFactory;
    private readonly ILogger<GetUserRequestHandler> _logger;

    public GetUserRequestHandler(IRepositoryFactory repositoryFactory, ILogger<GetUserRequestHandler> logger)
    {
        _repositoryFactory = repositoryFactory;
        _logger = logger;
    }

    public async Task<GetUserResponse> Handle(GetUserRequest request)
    {
        await using var repo = _repositoryFactory.Create<User>();

        var userResult = await repo.Read(user => user.UserId == request.UserId);

        if (!userResult.Any())
        {
            _logger.LogError($"Could not find a user for {request.UserId}");
            return new GetUserResponse
            {
                Success = false,
                Message = "No user could be found."
            };
        }

        var user = userResult.First();

        return new GetUserResponse
        {
            FirstName = user.FirstName ?? string.Empty,
            LastName = user.LastName ?? string.Empty,
            UserRating = user.UserRating,
            Success = true,
            Message = ""
        };
    }
}
