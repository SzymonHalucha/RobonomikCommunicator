using Microsoft.AspNetCore.Components;

namespace Client.Components.Widgets
{
    public partial class DeviceCard
    {
        [Parameter] public long Id { get; set; } = -1;
        [Parameter] public string Title { get; set; } = string.Empty;
        [Parameter] public string Description { get; set; } = string.Empty;

        public void OnConnectHandler()
        {
            Console.WriteLine("On Connection Handler");
        }
    }
}