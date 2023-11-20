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
            return await _runtime.InvokeAsync<bool>("isWebUSBSupported");
        }

        public async Task<USBDevice> AddDevice()
        {
            USBDevice device = await _runtime.InvokeAsync<USBDevice>("addDevice");
            return device;
        }

        public async Task<List<USBDevice>> GetDevicesList()
        {
            USBDevice[] devices = await _runtime.InvokeAsync<USBDevice[]>("getDevicesList");
            return devices.ToList();
        }
    }
}