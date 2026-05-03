using Microsoft.AspNetCore.Http;
using System.Text.Json;

namespace zaraz.Helpers
{
    public static class SessionExtensions
    {
        // Save object as JSON string in session
        public static void SetObjectAsJson(this ISession session, string key, object value)
        {
            if (value == null) 
                throw new ArgumentNullException(nameof(value), "Cannot store null value in session.");
            
            // Serialize the object to JSON and store it in session
            session.SetString(key, JsonSerializer.Serialize(value));
        }

        // Get object from JSON string stored in session
        public static T? GetObjectFromJson<T>(this ISession session, string key)
        {
            var value = session.GetString(key);
            
            if (string.IsNullOrEmpty(value))
            {
                return default; // Return default if session value is null or empty
            }
            
            try
            {
                // Deserialize the JSON string into an object of type T
                return JsonSerializer.Deserialize<T>(value);
            }
            catch (JsonException)
            {
                // Handle any errors in case of a deserialization issue
                // For now, we return default (could log the error as well if needed)
                return default;
            }
        }
    }
}
