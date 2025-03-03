using Identity.Configuration;
using Identity.DataAccess;
using Identity.DataAccess.Models;
using Identity.Schema.User.Auth;
using Identity.Util;
using Identity.Util.ConfigHelpers;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Pendo.IdentityService.Api.Commands;
using System.Text;

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
        .AddTransient<IJwtGenerator, JwtGenerator>()
        .AddTransient<IOtpHasher, OtpHasher>();

    public static IServiceCollection AddJwtAuthentication(this IServiceCollection services, IConfiguration configuration)
    {
        services.AddAuthentication(cfg =>
            {
                cfg.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
                cfg.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
                cfg.DefaultScheme = JwtBearerDefaults.AuthenticationScheme;
            }).AddJwtBearer(cfg =>
            {
                cfg.TokenValidationParameters = new()
                {
                    ValidateIssuer = true,
                    ValidateAudience = true,
                    ValidateLifetime = true,
                    ValidateIssuerSigningKey = true,
                    ValidIssuer = configuration[$"{nameof(JwtConfiguration)}:Issuer"],
                    ValidAudiences = [configuration[$"{nameof(JwtConfiguration)}:AppAudience"],
                                  configuration[$"{nameof(JwtConfiguration)}:ManagerAudience"]],
                    IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(configuration[$"{nameof(JwtConfiguration)}:SecretKey"]
                    ?? throw new ConfigurationException($"Configuration value {nameof(JwtConfiguration)}:SecretKey was null. App cannot start.")))
                };
            });

        return services.AddAuthorization();
    }

    public static IServiceCollection AddHandlers(this IServiceCollection services)
        => services
        .AddTransient<ICommandDispatcher, CommandDispatcher>()
        .AddTransient<ICommandHandler<OtpRequest, bool>, OtpRequestHandler>()
        .AddTransient<ICommandHandler<VerifyOtpRequest, VerifyOtpResponse>, VerifyOtpRequestHandler>();

    public static IServiceCollection AddDatabase(this IServiceCollection services, IConfiguration configuration)
        => services
        .AddDbContext<PendoDatabaseContext>(optionBuilder =>
        {
            optionBuilder.UseSqlServer(
                configuration[$"{nameof(IdentityConfiguration)}:ConnectionString"],
                options =>
                options.EnableRetryOnFailure(maxRetryCount: 5, maxRetryDelay: TimeSpan.FromSeconds(30), errorNumbersToAdd: null));
        })
        .AddScoped<IRepositoryFactory, RepositoryFactory>();

    public static IServiceCollection AddConfigurations(this IServiceCollection services, IConfigurationManager configuration)
        => services
        .Configure<IdentityConfiguration>(configuration.GetSection(nameof(IdentityConfiguration)))
        .Configure<OtpConfiguration>(configuration.GetSection(nameof(OtpConfiguration)))
        .Configure<JwtConfiguration>(configuration.GetSection(nameof(JwtConfiguration)));

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

    public static IConfigurationBuilder AddDbConfiguration(this WebApplicationBuilder builder)
    {
        builder.Services.AddTransient<DbConfigSource>();
        using var scope = builder.Services.BuildServiceProvider().CreateScope();

        var dbConfigSource = scope.ServiceProvider.GetRequiredService<DbConfigSource>();

        builder.Configuration.Sources.Add(dbConfigSource);
        return builder.Configuration;
    }
}