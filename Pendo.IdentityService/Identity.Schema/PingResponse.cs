namespace Identity.Schema;

/// <summary>
/// Response DTO for Ping requests.
/// </summary>
public class PingResponse : IRequest
{
    /// <summary>
    /// The message to return to the sender.
    /// </summary>
    public required string Message { get; set; }

    /// <summary>
    /// The time at which the response was sent.
    /// </summary>
    public DateTime TimeSent { get; set; }
}