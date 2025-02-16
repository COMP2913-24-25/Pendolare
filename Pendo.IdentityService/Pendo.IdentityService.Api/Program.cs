using Identity.DataAccess.Models;
using Pendo.IdentityService.Api;

var builder = WebApplication.CreateBuilder(args);

builder.AddFileConfiguration();

builder.Services
    .AddConfigurations(builder.Configuration)
    .AddDependencies()
    .AddDatabase(builder.Configuration)
    .AddHandlers()
    .AddControllers();

builder.Services
    .AddHealthChecks()
    .AddDbContextCheck<PendoDatabaseContext>();

// This must run after as it relies on the services.
builder.AddDbConfiguration();

builder.Services.AddJwtAuthentication(builder.Configuration);

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.MapHealthChecks("/healthcheck");

app.Run();
