using Identity.DataAccess.Models;
using Microsoft.Extensions.DependencyInjection;

namespace Identity.DataAccess;

/// <inheritdoc/>
public class RepositoryFactory : IRepositoryFactory
{
    private readonly IServiceProvider _serviceProvider;

    public RepositoryFactory(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public IRepository<TModel> Create<TModel>() where TModel : class
    {
        var context = _serviceProvider.GetRequiredService<PendoDatabaseContext>();
        return new Repository<TModel>(context);
    }
}