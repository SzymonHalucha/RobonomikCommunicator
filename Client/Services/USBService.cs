namespace Client.Services
{
    public class USBService : IUSBService
    {
        private readonly IJSRuntime _runtime;

        public USBService(IJSRuntime runtime)
        {
            _runtime = runtime;
        }

        public async Task<bool> IsSupported()
        {
            return await _runtime.InvokeAsync<bool>("isWebSerialSupported");
        }

        public async Task<USBDevice> AddDevice()
        {
            USBDevice device = await _runtime.InvokeAsync<USBDevice>("addUSBDevice");
            return device;
        }

        public async Task<USBDevice[]> GetDevicesList()
        {
            USBDevice[] devices = await _runtime.InvokeAsync<USBDevice[]>("getUSBDevicesList");
            return devices;
        }
    }
}