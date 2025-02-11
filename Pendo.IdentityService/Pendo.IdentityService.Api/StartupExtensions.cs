using Identity.Configuration;
using Identity.DataAccess.Models;
using Identity.Util;
using Microsoft.EntityFrameworkCore;

namespace Pendo.IdentityService.Api;

/// <summary>
/// Contains extensions for use in Program.cs.
/// </summary>
public static class StartupExtensions
{
    public static IServiceCollection AddDependencies(this IServiceCollection services)
        => services
        .AddEndpointsApiExplorer()
        .AddSwaggerGen()
        .AddTransient<IMailer, SendGridMailer>()
        .AddTransient<IDateTimeProvider, DateTimeProvider>()
        .AddTransient<IOtpGenerator, NumericOtpGenerator>()
        .AddTransient<IJwtGenerator, JwtGenerator>();

    public static IServiceCollection AddDatabase(this IServiceCollection services)
        => services.AddDbContext<PendoDatabaseContext>();

    public static IServiceCollection AddConfigurations(this IServiceCollection services, IConfigurationManager configuration)
        => services
        .Configure<IdentityConfiguration>(configuration.GetSection(nameof(IdentityConfiguration)))
        .Configure<OtpConfiguration>(configuration.GetSection(nameof(OtpConfiguration)));

    public static IConfigurationBuilder AddFileConfiguration(this WebApplicationBuilder builder)
    {
        builder.Configuration
            .SetBasePath(Directory.GetCurrentDirectory())
            .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);

        if (builder.Environment.IsDevelopment())
        {
            builder.Configuration.AddJsonFile("appsettings.Development.json", optional: true, reloadOnChange: true);
        }

        return builder.Configuration;
    }
}