namespace zaraz.Models
{
    public class Order
    {
        public int Id { get; set; }  // Add this line for the Id property
        public int UserId { get; set; }
        public string Address { get; set; }
        public string TransactionId { get; set; }
        public List<Product> Products { get; set; }
        public List<CartItem> Items { get; set; }
        public string Name { get; set; }
        public string Phone { get; set; }
        public string PaymentMethod { get; set; }

        // Constructor to ensure non-nullable properties are set
        public Order(int id, int userId, string address, string transactionId, List<Product> products, List<CartItem> items, string name, string phone, string paymentMethod)
        {
            Id = id;  // Initialize Id in constructor
            UserId = userId;
            Address = address ?? throw new ArgumentNullException(nameof(address)); 
            TransactionId = transactionId ?? throw new ArgumentNullException(nameof(transactionId)); 
            Products = products ?? throw new ArgumentNullException(nameof(products)); 
            Items = items ?? throw new ArgumentNullException(nameof(items)); 
            Name = name ?? throw new ArgumentNullException(nameof(name)); 
            Phone = phone ?? throw new ArgumentNullException(nameof(phone)); 
            PaymentMethod = paymentMethod ?? throw new ArgumentNullException(nameof(paymentMethod)); 
        }
    }

    // Your other classes remain unchanged...
}
