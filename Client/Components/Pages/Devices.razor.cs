using Microsoft.AspNetCore.Components;

namespace Client.Components.Pages
{
    public partial class Devices : ComponentBase
    {
        private string _devicesText = string.Empty;
        private string _first = string.Empty;
        private IUSBService? _usb;

        protected override void OnParametersSet()
        {
            _usb = Services?.GetService<IUSBService>();
            base.OnParametersSet();
        }

        private async Task OnAdd()
        {
            bool support = await _usb?.IsSupported()!;
            _devicesText = support.ToString();
            await _usb?.AddDevice()!;
        }

        private async Task OnList()
        {
            _first = "";
            var list = await _usb?.GetDevicesList()!;
            foreach (var item in list)
            {
                _first += $"{item.ManufacturerName}, {item.ProductName}, {item.ProductId}, {item.VendorId}";
                Console.WriteLine($"{item.ManufacturerName}, {item.ProductName}, {item.ProductId}, {item.VendorId}");
            }
        }
    }
}