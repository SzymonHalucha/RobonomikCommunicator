namespace Client.Components.Widgets
{
    public partial class DeviceCard
    {
        [Parameter] public required USBDevice Device { get; init; }

        protected string CustomName => string.IsNullOrEmpty(Device.CustomName) ? "Default" : Device.CustomName;
        protected string DeviceName => string.IsNullOrEmpty(Device.DeviceName) ? "Default" : Device.DeviceName;
        protected string Manufacturer => string.IsNullOrEmpty(Device.ManufacturerName) ? "Default" : Device.ManufacturerName;
        protected string SerialNumber => string.IsNullOrEmpty(Device.SerialNumber) ? "Default" : Device.SerialNumber;

        private void OnConnectHandler()
        {
            Device.IsConnected = !Device.IsConnected;
        }
    }
}