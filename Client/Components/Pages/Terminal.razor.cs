namespace Client.Components.Pages
{
    public partial class Terminal : ComponentBase
    {
        [Inject] public required IUSBService USBService { get; init; }


        protected override async Task OnInitializedAsync()
        {
            await USBService.RefreshAvailableSerialsAsync();
        }
    }
}