global using Microsoft.AspNetCore.Components;
global using Server.Components;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddRazorComponents().AddInteractiveServerComponents().AddInteractiveWebAssemblyComponents();

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
    .AddAdditionalAssemblies(typeof(Client.Components._Imports).Assembly);

await host.RunAsync();