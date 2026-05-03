namespace zaraz.Models
{
    public class CartItem
    {
        // Properties for the cart item
        public int ProductId { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public string ImageUrl { get; set; }

        // If ProductName was required in the past and needs to be initialized
        public string ProductName { get; set; }

        // Optionally, you can add more properties like Quantity, Price, etc.
        public int Quantity { get; set; }
        public decimal Price { get; set; }

        // Constructor to initialize CartItem object with all necessary details
        public CartItem(int productId, string name, string description, string imageUrl, string productName, int quantity, decimal price)
        {
            // Argument null checks for required properties
            ProductId = productId;
            Name = name ?? throw new ArgumentNullException(nameof(name));
            Description = description ?? string.Empty; // Default to empty string if null
            ImageUrl = imageUrl ?? string.Empty; // Default to empty string if null
            ProductName = productName ?? throw new ArgumentNullException(nameof(productName));
            Quantity = quantity;
            Price = price;
        }

        // Total Price based on quantity and price
        public decimal TotalPrice => Quantity * Price;
    }
}
