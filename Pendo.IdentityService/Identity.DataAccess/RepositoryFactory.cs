using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Identity.DataAccess;

/// <inheritdoc/>
public class RepositoryFactory : IRepositoryFactory
{
    public IRepository<TModel> Create<TModel>() where TModel : class
    {
        throw new NotImplementedException();
    }
}
