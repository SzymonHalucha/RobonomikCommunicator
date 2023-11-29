namespace Client.Models
{
    public sealed class ConnectDeviceEventArgs(bool success) : EventArgs
    {
        public bool Success { get; init; } = success;
    }

    public sealed class DisconnectDeviceEventArgs(bool success) : EventArgs
    {
        public bool Success { get; init; } = success;
    }

    public sealed class SendMessageEventArgs(long timestamp, string message, bool success) : EventArgs
    {
        public long Timestamp { get; init; } = timestamp;
        public string Message { get; init; } = message;
        public bool Success { get; init; } = success;
    }

    public sealed class MessageReceivedEventArgs(long timestamp, string message) : EventArgs
    {
        public long Timestamp { get; init; } = timestamp;
        public string Message { get; init; } = message;
    }

    public class USBDevice
    {
        public bool IsConnected { get; set; } = false;
        public int SerialBaudrate { get; set; } = 9600;
        public string CustomName { get; set; } = "Default";
        public IJSObjectReference? SerialPort { get; set; }

        public required string ManufacturerName { get; init; }
        public required string SerialNumber { get; init; }
        public required string ProductName { get; init; }
        public required int ProductId { get; init; }
        public required int VendorId { get; init; }

        public EventHandler<ConnectDeviceEventArgs>? OnConnect;
        public EventHandler<DisconnectDeviceEventArgs>? OnDisconnect;
        public EventHandler<SendMessageEventArgs>? OnMessageSend;
        public EventHandler<MessageReceivedEventArgs>? OnMessageReceived;

        public static readonly USBDevice None = new()
        {
            ManufacturerName = "",
            SerialNumber = "",
            ProductName = "",
            ProductId = 0,
            VendorId = 0,
        };

        public override int GetHashCode()
        {
            return HashCode.Combine(ManufacturerName, SerialNumber, ProductName, ProductId, VendorId);
        }

        public override bool Equals(object? obj)
        {
            return obj is USBDevice other
                   && ManufacturerName == other.ManufacturerName
                   && SerialNumber == other.SerialNumber
                   && ProductName == other.ProductName
                   && ProductId == other.ProductId
                   && VendorId == other.VendorId;
        }

        public static bool operator ==(USBDevice left, USBDevice right)
        {
            return left.Equals(right);
        }

        public static bool operator !=(USBDevice left, USBDevice right)
        {
            return !left.Equals(right);
        }
    }
}