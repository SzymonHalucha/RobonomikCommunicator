namespace Client.Components.Widgets
{
    public partial class DeviceCard : ComponentBase
    {
        [Parameter] public required USBDevice Device { get; init; }
        [Inject] public required IUSBService USBService { get; init; }

        protected string Manufacturer => string.IsNullOrEmpty(Device.ManufacturerName) ? "Default" : Device.ManufacturerName;
        protected string SerialNumber => string.IsNullOrEmpty(Device.SerialNumber) ? "Default" : Device.SerialNumber;
        protected string ProductName => string.IsNullOrEmpty(Device.ProductName) ? "Default" : Device.ProductName;

        private async Task OnConnectHandler()
        {
            if (!Device.IsConnected)
            {
                await USBService.OpenSerialAsync(Device);
                Device.OnMessageSend += (sender, evt) => { Console.WriteLine($"Sended: {evt.Message}"); };
                Device.OnMessageReceived += (sender, evt) => { Console.WriteLine($"Recieved: {evt.Message}"); };
            }
            else
            {
                await USBService.CloseSerialAsync(Device);
            }

            StateHasChanged();
        }

        private async Task OnSendMessageHandler()
        {
            await USBService.WriteToSerialAsync(Device, "Testowy\r\n");
        }

        private async Task OnRecieveMessageHandler()
        {
            await USBService.ListenToSerialAsync(Device);
        }
    }
}