global using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
global using Microsoft.AspNetCore.Components;
global using Microsoft.JSInterop;
global using Client.Services;
global using Client.Models;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.Services.AddSingleton<IUSBService, USBService>();
var host = builder.Build();
await host.RunAsync();