namespace Shared.Components
{
    public partial class DeviceCard : ComponentBase
    {
        [Parameter] public required IConnection Device { get; init; }
        [Inject] public required ISerialService SerialService { get; init; }

        protected string ConnectionName => Device.ConnectionName;
        protected string ConnectionAddress => Device.ConnectionAddress;
        protected bool IsAvailable => Device.IsAvailable;

        private void OnConnectionHandler()
        {
            if (Device.IsAvailable)
            {
                SerialService.Disconnect((SerialConnection)Device);
                SerialService.OnMessageRecieved -= OnMessageRecieved;
            }
            else
            {
                SerialService.Connect((SerialConnection)Device);
                SerialService.OnMessageRecieved += OnMessageRecieved;
            }

            StateHasChanged();
        }

        private void OnMessageSendHandler()
        {
            SerialService.SendMessageToDevice((SerialConnection)Device, "Dupa");
        }

        private void OnMessageRecieved(object? sender, SerialMessageEventArgs args)
        {
            if (args.Connection == Device)
            {
                Console.WriteLine($"Readed: {args.Message}");
            }
        }
    }
}