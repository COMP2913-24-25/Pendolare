using Identity.DataAccess.Models;
using Microsoft.EntityFrameworkCore;
using System.Linq.Expressions;

namespace Identity.DataAccess;

/// <inheritdoc/>
public class Repository<TModel> : IRepository<TModel> where TModel : class
{
    private readonly DbContext _dbContext;
    private readonly DbSet<TModel> _dbSet;

    public Repository(DbContext dbContext)
    {
        _dbContext = dbContext;
        _dbSet = _dbContext.Set<TModel>();
    }

    public async Task Create(TModel model, bool saveOnComplete = true)
    {
        await _dbContext.AddAsync(model);
        await SaveOnComplete(saveOnComplete);
    }

    public async Task Delete(TModel model, bool saveOnComplete = true)
    {
        _dbContext.Remove(model);
        await SaveOnComplete(saveOnComplete);
    }

    public IEnumerable<TModel> Read(Expression<Func<TModel, bool>>? filter = null)
    {
        if (filter is null)
            return _dbSet.ToList();

        return _dbSet.AsQueryable().Where(filter).ToList();
    }

    public async Task Update(TModel model, bool saveOnComplete = true)
    {
        _dbContext.Update(model);
        await SaveOnComplete(saveOnComplete);
    }

    public async ValueTask DisposeAsync()
        => await _dbContext.DisposeAsync();

    private async Task SaveOnComplete(bool saveOnComplete)
    {
        if (!saveOnComplete) return;

        await _dbContext.SaveChangesAsync();
    }
}
