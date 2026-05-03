using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using zaraz.Helpers;
using zaraz.Services;
using zaraz.Models;
using System.Linq;
using System.Collections.Generic;
using System;
using System.IO;

namespace zaraz.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly PdfVoucherService _pdfVoucherService;

        // Constructor for HomeController
        public HomeController(ILogger<HomeController> logger, PdfVoucherService pdfVoucherService)
        {
            _logger = logger;
            _pdfVoucherService = pdfVoucherService;
        }

        // Index action that displays a list of products (limiting to the first 15 items)
        public IActionResult Index()
        {
            var products = GetProducts().Take(15).ToList();
            return View(products); // Passing the products to the view
        }

        // Privacy page view
        public IActionResult Privacy() => View();

        // Cart page view
        public IActionResult Cart()
        {
            var cart = HttpContext.Session.GetObjectFromJson<List<CartItem>>("Cart") ?? new List<CartItem>();
            return View(cart); // Passing the cart items to the view
        }

        // Add product to the cart
        [HttpPost]
        public IActionResult AddToCart(int productId)
        {
            var product = GetProductById(productId);
            if (product == null) return RedirectToAction("Index");

            var cart = HttpContext.Session.GetObjectFromJson<List<CartItem>>("Cart") ?? new List<CartItem>();
            var existingItem = cart.FirstOrDefault(x => x.ProductId == productId);

            if (existingItem != null)
            {
                existingItem.Quantity++; 
            }
            else
            {
                cart.Add(new CartItem(
                    productId, product.Name, product.Description, product.ImageUrl, 
                    "Default Category", 1, product.Price));
            }

            HttpContext.Session.SetObjectAsJson("Cart", cart);
            return RedirectToAction("Cart");
        }

        // Remove a product from the cart
        [HttpPost]
        public IActionResult RemoveFromCart(int productId)
        {
            var cart = HttpContext.Session.GetObjectFromJson<List<CartItem>>("Cart") ?? new List<CartItem>();
            var itemToRemove = cart.FirstOrDefault(p => p.ProductId == productId);
            if (itemToRemove != null)
            {
                cart.Remove(itemToRemove);
                HttpContext.Session.SetObjectAsJson("Cart", cart);
            }

            return RedirectToAction("Cart");
        }

        private Product? GetProductById(int productId)
        {
            var products = GetProducts();
            return products.FirstOrDefault(p => p.ProductId == productId);
        }

        private List<Product> GetProducts()
        {
            return new List<Product>
            {
                new Product(1, "Product1", "Laptop", "/images/product1.jpg", 10.99m, 100),
                new Product(2, "Product2", "Mouse", "/images/product2.jpg", 20.99m, 50),
                new Product(3, "Product3", "Cable", "/images/product3.jpg", 30.99m, 30),
                new Product(4, "Product4", "Ram", "/images/product4.jpg", 15.99m, 75),
                new Product(5, "Product5", "CPU", "/images/product5.jpg", 25.99m, 120),
                new Product(6, "Product6", "Monitor", "/images/product6.jpg", 35.99m, 10),
                new Product(7, "Product7", "Apple iphone", "/images/product7.jpg", 40.99m, 60),
                new Product(8, "Product8", "Iphone 15", "/images/product8.jpg", 50.99m, 80),
                new Product(9, "Product9", "Iphone 15 pro max", "/images/product9.jpg", 45.99m, 50),
                new Product(10, "Product10", "Iphone 16", "/images/product10.jpg", 55.99m, 40),
                new Product(11, "Product11", "Iphone 16 pro", "/images/product11.jpg", 60.99m, 30),
                new Product(12, "Product12", "Iphone 16 pro max", "/images/product12.jpg", 65.99m, 70),
                new Product(13, "Product13", "Samsung S23 Ultra", "/images/product13.jpg", 70.99m, 100),
                new Product(14, "Product14", "Samsung S24 Ultra", "/images/product14.jpg", 75.99m, 60),
                new Product(15, "Product15", "Samsung S25", "/images/product15.jpg", 80.99m, 90)
            };
        }

        // Checkout page (GET request)
        [HttpGet]
        public IActionResult Checkout() => View();

        // Process checkout (POST request)
        [HttpPost]
        public IActionResult Checkout(string Name, string Phone, string Address, string PaymentMethod)
        {
            TempData["Name"] = Name;
            TempData["Phone"] = Phone;
            TempData["Address"] = Address;
            TempData["PaymentMethod"] = PaymentMethod;

            // Redirect based on the payment method selected
            return PaymentMethod switch
            {
                "Bkash" => RedirectToAction("ProcessBkash"),
                "Card" => RedirectToAction("ProcessCard"),
                "Cash" => RedirectToAction("ProcessCash"),
                _ => View("Checkout")
            };
        }

        // Payment method views
        public IActionResult ProcessBkash() => View();
        public IActionResult ProcessCard() => View();
        public IActionResult ProcessCash() => View();

        // Process payment and generate PDF voucher
        [HttpPost]
        public IActionResult ProcessPayment(string customerName, string phone, string address, string paymentMethod, string bkashNumber = "", decimal? amount = null)
        {
            var cart = HttpContext.Session.GetObjectFromJson<List<CartItem>>("Cart") ?? new List<CartItem>();
            if (string.IsNullOrWhiteSpace(customerName) || !cart.Any())
            {
                return BadRequest("Invalid input or empty cart.");
            }

            // Convert cart items to product data
            var products = cart.Select(c => new Product(
                c.ProductId,
                c.Name,
                c.Description,
                c.ImageUrl,
                c.Price,
                c.Quantity
            )).ToList();

            // Calculate the total amount for the cart
            decimal totalAmount = products.Sum(p => p.Price * p.Quantity);

            // Add payment details
            string paymentDetails = paymentMethod == "Bkash" 
                ? $"Bkash Number: {bkashNumber}, Amount: {amount}" 
                : paymentMethod == "Cash" 
                ? "Cash on Delivery" 
                : "Card Payment";

            // Generate a transaction ID and user ID
            string userId = User.Identity?.Name ?? "Guest";
            string transactionId = Guid.NewGuid().ToString();

            // Generate the PDF voucher using PdfVoucherService
            var pdfBytes = _pdfVoucherService.GenerateVoucherPdf(
                "Zaraz Online Store",
                customerName,
                phone,
                address,
                paymentDetails,
                products,
                totalAmount,
                userId,
                transactionId
            );

            // Create a safe filename for the PDF
            string safeName = string.Join("_", customerName.Split(Path.GetInvalidFileNameChars()));
            string fileName = $"{safeName}_Voucher_{DateTime.Now:yyyyMMddHHmmss}.pdf";

            // Return the PDF file
            return File(pdfBytes, "application/pdf", fileName);
        }

        // Error handling for the application
        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            string requestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier ?? "Unknown";
            return View(new ErrorViewModel { RequestId = requestId });
        }
    }
}
