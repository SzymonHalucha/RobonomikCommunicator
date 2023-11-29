namespace Client.Services
{
    public interface IUSBService
    {
        public List<USBDevice> AvailableSerials { get; }
        public bool IsSupported { get; }
        public Task GetPermissionAsync();
        public Task RefreshAvailableSerialsAsync();
        public Task OpenSerialAsync(USBDevice device);
        public Task CloseSerialAsync(USBDevice device);
        public Task WriteToSerialAsync(USBDevice device, string message);
        public Task ListenToSerialAsync(USBDevice device);
        public void StopListenToSerial(USBDevice device);
    }
}