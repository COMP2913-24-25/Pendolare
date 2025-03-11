using System.Linq.Expressions;

namespace Identity.DataAccess;

/// <summary>
/// Provides a set of CRUD operations to interact with the database, abstracting the underlying EF Core code.
/// </summary>
/// <typeparam name="TModel">The type of model to query.</typeparam>
public interface IRepository<TModel> : IAsyncDisposable where TModel : class
{
    /// <summary>
    /// Retrieves all models matching the <paramref name="filter"/>.
    /// </summary>
    /// <param name="filter">Boolean predicate filter to filter records by.</param>
    /// <returns>An enumerable of <see cref="{TModel}"/>.</returns>
    Task<IEnumerable<TModel>> Read(Expression<Func<TModel, bool>>? filter = null);

    /// <summary>
    /// Updates a database record.
    /// </summary>
    /// <param name="model">The updated model.</param>
    /// <param name="saveOnComplete">Decides whether to immediately commit the update operation or wait to manually commit the transaction.</param>
    /// <returns></returns>
    Task Update(TModel model, bool saveOnComplete = true);

    /// <summary>
    /// Creates a new database record.
    /// </summary>
    /// <param name="model">The new model.</param>
    /// <param name="saveOnComplete">Decides whether to immediately commit the insert operation or wait to manually commit the transaction.</param>
    /// <returns></returns>
    Task Create(TModel model, bool saveOnComplete = true);


    /// <summary>
    /// Deletes a database record.
    /// </summary>
    /// <param name="model">The model to delete.</param>
    /// <param name="saveOnComplete">Decides whether to immediately commit the delete operation or wait to manually commit the transaction.</param>
    /// <returns></returns>
    Task Delete(TModel model, bool saveOnComplete = true);
}