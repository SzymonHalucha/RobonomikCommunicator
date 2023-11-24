namespace Client.Models
{
    public class USBDevice
    {
        public bool IsConnected { get; set; } = false;
        public int SerialBaudrate { get; set; } = 9600;
        public string CustomName { get; set; } = "Default";

        public required string ManufacturerName { get; init; }
        public required string SerialNumber { get; init; }
        public required string DeviceName { get; init; }
        public required int DeviceId { get; init; }
        public required int VendorId { get; init; }

        public override int GetHashCode()
        {
            return HashCode.Combine(ManufacturerName, SerialNumber, DeviceName, DeviceId, VendorId);
        }

        public override bool Equals(object? obj)
        {
            return obj is USBDevice other
                   && ManufacturerName == other.ManufacturerName
                   && SerialNumber == other.SerialNumber
                   && DeviceName == other.DeviceName
                   && DeviceId == other.DeviceId
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