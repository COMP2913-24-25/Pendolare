namespace Identity.Util;

public interface IJwtGenerator
{
    string GenerateJwt(string userEmail, bool isManager);
}
