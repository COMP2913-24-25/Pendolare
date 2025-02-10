using Pendo.IdentityService.Api;

var builder = WebApplication.CreateBuilder(args);

builder.AddFileConfiguration();

builder.Services.AddConfigurations(builder.Configuration);
builder.Services.AddControllers();
builder.Services.AddDependencies();

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
