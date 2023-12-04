namespace Shared.Models.Connections
{
    public interface IConnection
    {
        public Guid Id { get; }
        public bool IsAvailable { get; }
        public string ConnectionName { get; }
        public string ConnectionAddress { get; }
        public string CustomName { get; set; }
    }
}