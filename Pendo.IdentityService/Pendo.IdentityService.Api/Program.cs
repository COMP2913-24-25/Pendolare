using Pendo.IdentityService.Api;

var builder = WebApplication.CreateBuilder(args);

builder.AddFileConfiguration();

builder.Services.AddConfigurations(builder.Configuration)
    .AddDependencies()
    .AddDatabase()
    .AddControllers();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
