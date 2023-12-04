namespace Client
{
    public class Program
    {
        private static async Task Main(string[] args)
        {
            var builder = WebAssemblyHostBuilder.CreateDefault(args);
            var host = builder.Build();
            await host.RunAsync();
        }
    }
}