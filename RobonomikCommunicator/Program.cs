using RobonomikCommunicator.Components;

namespace RobonomikCommunicator
{
    public class Program
    {
        public static void Main(string[] args)
        {
            WebApplication app = ManageBuilder(args);
            ManageDebug(app);
            ManageApp(app);
            app.Run();
        }

        private static WebApplication ManageBuilder(string[] args)
        {
            WebApplicationBuilder builder = WebApplication.CreateBuilder(args);
            builder.Services.AddRazorComponents().AddInteractiveServerComponents().AddInteractiveWebAssemblyComponents();
            builder.Services.AddControllers();
            return builder.Build();
        }

        private static void ManageDebug(WebApplication app)
        {
            if (app.Environment.IsDevelopment())
            {
                app.UseWebAssemblyDebugging();
            }
            else
            {
                app.UseExceptionHandler("/error");
                app.UseHsts();
            }
        }

        private static void ManageApp(WebApplication app)
        {
            app.UseHttpsRedirection();
            app.UseStaticFiles();
            app.UseAntiforgery();
            app.MapRazorComponents<App>().AddInteractiveServerRenderMode().AddInteractiveWebAssemblyRenderMode();
        }
    }
}