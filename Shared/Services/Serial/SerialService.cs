using System.Collections.Immutable;
using System.IO.Ports;

namespace Shared.Services.Serial
{
    public class SerialConnectionEventArgs(SerialConnection connection) : EventArgs
    {
        public SerialConnection Connection { get; init; } = connection;
    }

    public class SerialErrorEventArgs(Exception exception, SerialConnection connection) : EventArgs
    {
        public Exception Exception { get; init; } = exception;
        public SerialConnection Connection { get; init; } = connection;
    }

    public class SerialMessageEventArgs(SerialConnection connection, long timestamp, string message) : EventArgs
    {
        public Guid Id = Guid.NewGuid();
        public SerialConnection Connection { get; init; } = connection;
        public long Timestamp { get; init; } = timestamp;
        public string Message { get; init; } = message;
    }

    public class SerialService : ISerialService
    {
        public List<SerialConnection> AvailableConnections { get; private set; } = [];

        public event EventHandler<SerialConnectionEventArgs>? OnSerialConnected;
        public event EventHandler<SerialConnectionEventArgs>? OnSerialDisconnected;
        // public event EventHandler<SerialErrorEventArgs>? OnSerialError;
        public event EventHandler<SerialMessageEventArgs>? OnMessageSended;
        public event EventHandler<SerialMessageEventArgs>? OnMessageRecieved;

        public void Refresh()
        {
            var ports = SerialPort.GetPortNames();
            var unavailable = AvailableConnections.Where(conn => !ports.Any(port => port == conn.Port.PortName)).ToImmutableArray();
            var newPorts = ports.Where(port => !AvailableConnections.Any(conn => conn.Port.PortName == port)).ToImmutableArray();

            foreach (string portName in newPorts)
            {
                SerialPort port = new(portName, 9600);
                SerialConnection connection = new(Guid.NewGuid(), port);
                AvailableConnections.Add(connection);
            }

            foreach (SerialConnection connection in unavailable)
            {
                AvailableConnections.Remove(connection);
                connection.Port?.Dispose();
            }
        }

        public bool Connect(SerialConnection connection)
        {
            connection.Port.Open();
            connection.Port.DataReceived += SerialDataRecivedHandler;
            OnSerialConnected?.Invoke(this, new(connection));
            return true;
        }

        public bool Disconnect(SerialConnection connection)
        {
            if (connection.IsAvailable) connection.Port.Close();
            connection.Port.DataReceived -= SerialDataRecivedHandler;
            OnSerialDisconnected?.Invoke(this, new(connection));
            return true;
        }

        public bool SendMessageToDevice(SerialConnection connection, string message)
        {
            connection.Port.WriteLine(message);
            OnMessageSended?.Invoke(this, new(connection, DateTime.Now.Ticks, message));
            return true;
        }

        public SerialConnection? GetConnectionById(Guid id)
        {
            return AvailableConnections.FirstOrDefault(x => x.Id.Equals(id));
        }

        public SerialConnection? GetConnectionByPort(string portName)
        {
            return AvailableConnections.FirstOrDefault(x => x.ConnectionAddress.Equals(portName));
        }

        public SerialConnection? GetConnectionByCustomName(string customName)
        {
            return AvailableConnections.FirstOrDefault(x => x.CustomName.Equals(customName));
        }

        private void SerialDataRecivedHandler(object sender, SerialDataReceivedEventArgs args)
        {
            SerialPort port = (SerialPort)sender;
            SerialConnection connection = GetConnectionByPort(port.PortName)!;
            OnMessageRecieved?.Invoke(this, new(connection, DateTime.Now.Ticks, port.ReadLine()));
        }
    }
}