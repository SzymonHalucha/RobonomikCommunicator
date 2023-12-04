using System.IO.Ports;

namespace Shared.Models.Connections
{
    public class SerialConnection(Guid id, SerialPort port, string customName = "Default") : IConnection
    {
        public Guid Id { get; init; } = id;
        public bool IsAvailable => Port.IsOpen;
        public string ConnectionName => Port.PortName;
        public string ConnectionAddress => Port.PortName;
        public string CustomName { get; set; } = customName;

        public SerialPort Port { get; init; } = port;
        public int Baudrate => Port.BaudRate;
    }
}