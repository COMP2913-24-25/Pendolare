using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Identity.Schema;

/// <summary>
/// Provides a basic response that can be extended.
/// </summary>
public class Response
{
    /// <summary>
    /// Indicates whether the request was successful or not.
    /// </summary>
    public bool Success { get; set; } = true;

    /// <summary>
    /// The message returned with the response. Can be left empty.
    /// </summary>
    public string Message { get; set; } = string.Empty;

    /// <summary>
    /// Creates a failure response with a given message.
    /// </summary>
    public static Response FailureResponse(string message)
        => new()
        { 
            Success = false,
            Message = message
        };

    public static Response SuccessResponse(string message = "")
        => new()
        {
            Message = message
        };
}