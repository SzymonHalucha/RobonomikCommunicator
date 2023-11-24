namespace Client.Services
{
    public interface IUSBService
    {
        public Task<bool> IsSupported();
        public Task<USBDevice> AddDevice();
        public Task<USBDevice[]> GetDevicesList();
    }
}