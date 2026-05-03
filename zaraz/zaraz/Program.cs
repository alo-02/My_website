using Microsoft.Extensions.Configuration;
using MySql.Data.MySqlClient;
using zaraz.Services; // Ensure you have this if PdfVoucherService is in this namespace

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

// Register the MySQL database connection using the connection string from appsettings.json
builder.Services.AddSingleton<MySqlConnection>(provider =>
{
    var connectionString = builder.Configuration.GetConnectionString("MySqlConnection");
    return new MySqlConnection(connectionString);
});

// Register the PdfVoucherService in DI container
builder.Services.AddScoped<PdfVoucherService>();

// Add session support
builder.Services.AddDistributedMemoryCache();  // In-memory cache to store session data
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(30); // Set session timeout
    options.Cookie.HttpOnly = true; // Make the session cookie HttpOnly
    options.Cookie.IsEssential = true; // Mark the cookie as essential for the app
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

// Add UseSession in the middleware pipeline
app.UseSession();

app.UseRouting();

// Default route configuration
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
