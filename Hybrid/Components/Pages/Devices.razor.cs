namespace Hybrid.Components.Pages
{
    public partial class Devices : ComponentBase
    {
        [Inject] public required ISerialService SerialService { get; init; }

        private List<SerialConnection> Connections => SerialService.AvailableConnections;

        protected override void OnInitialized()
        {
            SerialService.Refresh();
            StateHasChanged();
        }

        private void OnRefreshHandler()
        {
            SerialService.Refresh();
            StateHasChanged();
        }
    }
}