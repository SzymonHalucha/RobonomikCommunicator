namespace Client.Components.Pages
{
    public partial class Devices : ComponentBase
    {
        [Inject] public required IUSBService USBService { get; init; }

        private bool IsSupported => USBService.IsSupported;
        private List<USBDevice> AvailableSerials => USBService.AvailableSerials;

        protected override async Task OnInitializedAsync()
        {
            await USBService.RefreshAvailableSerialsAsync();
        }

        private async Task OnRefreshHandler()
        {
            await USBService.RefreshAvailableSerialsAsync();
            StateHasChanged();
        }

        private async Task OnAddHandler()
        {
            await USBService.GetPermissionAsync();
            await OnRefreshHandler();
        }
    }
}