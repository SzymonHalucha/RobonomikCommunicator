namespace Server
{
    public class Program
    {
        private static async Task Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);
            builder.Services.AddRazorComponents()
                            .AddInteractiveServerComponents()
                            .AddInteractiveWebAssemblyComponents();

            var host = builder.Build();

            if (host.Environment.IsDevelopment())
            {
                host.UseWebAssemblyDebugging();
            }
            else
            {
                host.UseExceptionHandler("/Error");
                host.UseHsts();
            }

            host.UseHttpsRedirection();
            host.UseStaticFiles();
            host.UseAntiforgery();
            host.UseStatusCodePages();
            host.UseStatusCodePagesWithRedirects("/Error/{0}");

            host.MapRazorComponents<App>()
                .AddInteractiveServerRenderMode()
                .AddInteractiveWebAssemblyRenderMode()
                .AddAdditionalAssemblies(typeof(Client.Program).Assembly);

            await host.RunAsync();
        }
    }
}