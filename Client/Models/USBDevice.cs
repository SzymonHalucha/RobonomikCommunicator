namespace Client.Models
{
    public struct USBDevice
    {
        public string ManufacturerName { get; init; }
        public string ProductName { get; init; }
        public int ProductId { get; init; }
        public int VendorId { get; init; }
    }
}