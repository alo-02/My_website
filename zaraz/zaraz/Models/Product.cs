namespace zaraz.Models
{
    public class Product
    {
        public int ProductId { get; set; }  // Unique Product ID
        public string Name { get; set; }
        public string Description { get; set; }  // Added Description
        public string ImageUrl { get; set; }    // Added ImageUrl
        public decimal Price { get; set; }
        public int Quantity { get; set; }   // Quantity of the product in stock

        // Constructor to ensure required fields are initialized
        public Product(int productId, string name, string description, string imageUrl, decimal price, int quantity)
        {
            ProductId = productId;
            Name = name;
            Description = description;
            ImageUrl = imageUrl;
            Price = price;
            Quantity = quantity;
        }
    }
}
