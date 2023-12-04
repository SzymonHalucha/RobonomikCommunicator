namespace Shared.Services.Serial
{
    public interface ISerialService
    {
        public List<SerialConnection> AvailableConnections { get; }

        public event EventHandler<SerialConnectionEventArgs>? OnSerialConnected;
        public event EventHandler<SerialConnectionEventArgs>? OnSerialDisconnected;
        // public event EventHandler<SerialErrorEventArgs>? OnSerialError;
        public event EventHandler<SerialMessageEventArgs>? OnMessageSended;
        public event EventHandler<SerialMessageEventArgs>? OnMessageRecieved;

        public void Refresh();
        public bool Connect(SerialConnection connection);
        public bool Disconnect(SerialConnection connection);
        public bool SendMessageToDevice(SerialConnection connection, string message);

        public SerialConnection? GetConnectionById(Guid id);
        public SerialConnection? GetConnectionByPort(string portName);
        public SerialConnection? GetConnectionByCustomName(string customName);
    }
}