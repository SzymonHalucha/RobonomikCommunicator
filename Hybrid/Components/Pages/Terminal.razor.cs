namespace Hybrid.Components.Pages
{
    public partial class Terminal : ComponentBase
    {
        [Inject] public required ISerialService SerialService { get; init; }
    }
}