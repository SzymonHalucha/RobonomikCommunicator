global using Microsoft.AspNetCore.Components;
global using Server.Components;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddRazorComponents().AddInteractiveServerComponents().AddInteractiveWebAssemblyComponents();
builder.Services.AddControllers();

var host = builder.Build();
host.UseHttpsRedirection();
host.UseStaticFiles();
host.UseStatusCodePages();
host.UseAntiforgery();
host.UseStatusCodePagesWithRedirects("/Error/{0}");
host.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode()
    .AddInteractiveWebAssemblyRenderMode()
    .AddAdditionalAssemblies(typeof(Client.Components._Imports).Assembly);

if (host.Environment.IsDevelopment())
{
    host.UseWebAssemblyDebugging();
}
else
{
    host.UseExceptionHandler("/Error");
    host.UseHsts();
}

await host.RunAsync();
