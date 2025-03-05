namespace Identity.DataAccess;

/// <summary>
/// Used to produce new <see cref="IRepository{TModel}"/> instances.
/// </summary>
public interface IRepositoryFactory
{
    /// <summary>
    /// Produces a new repository instance.
    /// </summary>
    /// <typeparam name="TModel"></typeparam>
    /// <returns></returns>
    IRepository<TModel> Create<TModel>() where TModel : class;
}