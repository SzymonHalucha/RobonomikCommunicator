namespace Client.Components.Pages
{
    public partial class Devices : ComponentBase
    {
        [Inject] protected IUSBService? USBService { get; init; }

        protected USBDevice[] Ports = [];

        protected override async Task OnInitializedAsync()
        {
            Ports = await USBService?.GetDevicesList()! ?? [];
        }

        private async Task OnRefreshHandler()
        {
            Ports = await USBService?.GetDevicesList()! ?? [];
            StateHasChanged();
        }
    }
}