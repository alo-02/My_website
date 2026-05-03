using System;
using System.Collections.Generic;
using System.IO;
using iText.Kernel.Pdf;
using iText.Layout;
using iText.Layout.Element;
using iText.Layout.Properties;
using iText.Kernel.Font;
using iText.IO.Font.Constants;
using zaraz.Models;

namespace zaraz.Services
{
    public class PdfVoucherService
    {
        public byte[] GenerateVoucherPdf(
            string companyName,
            string customerName,
            string phone,
            string address,
            string paymentMethod,
            List<Product> products,
            decimal totalAmount,
            string userId,
            string transactionId)
        {
            using (MemoryStream memoryStream = new MemoryStream())
            {
                // Create PDF document and writer
                PdfWriter writer = new PdfWriter(memoryStream);
                PdfDocument pdf = new PdfDocument(writer);
                Document document = new Document(pdf);

                // Fonts
                PdfFont boldFont = PdfFontFactory.CreateFont(StandardFonts.HELVETICA_BOLD);
                PdfFont normalFont = PdfFontFactory.CreateFont(StandardFonts.HELVETICA);
                PdfFont italicFont = PdfFontFactory.CreateFont(StandardFonts.HELVETICA_OBLIQUE);

                // Header
                document.Add(new Paragraph(companyName)
                    .SetFont(boldFont)
                    .SetTextAlignment(TextAlignment.CENTER)
                    .SetFontSize(18));

                document.Add(new Paragraph($"Date: {DateTime.Now:yyyy-MM-dd HH:mm}")
                    .SetFont(normalFont)
                    .SetTextAlignment(TextAlignment.RIGHT));

                document.Add(new Paragraph($"Transaction ID: {transactionId}")
                    .SetFont(boldFont)
                    .SetFontSize(12));

                document.Add(new Paragraph($"User ID: {userId}")
                    .SetFont(normalFont)
                    .SetFontSize(12));

                // Customer Info
                document.Add(new Paragraph("\nCustomer Information:").SetFont(boldFont));
                document.Add(new Paragraph($"Name: {customerName}").SetFont(normalFont));
                document.Add(new Paragraph($"Phone: {phone}").SetFont(normalFont));
                document.Add(new Paragraph($"Address: {address}").SetFont(normalFont));
                document.Add(new Paragraph($"Payment Method: {paymentMethod}").SetFont(normalFont));

                // Product Table
                document.Add(new Paragraph("\nProduct Details:").SetFont(boldFont));

                Table table = new Table(UnitValue.CreatePercentArray(new float[] { 4, 2, 2, 2 }))
                    .UseAllAvailableWidth();

                table.AddHeaderCell(new Cell().Add(new Paragraph("Product Name").SetFont(boldFont)));
                table.AddHeaderCell(new Cell().Add(new Paragraph("Quantity").SetFont(boldFont)));
                table.AddHeaderCell(new Cell().Add(new Paragraph("Price").SetFont(boldFont)));
                table.AddHeaderCell(new Cell().Add(new Paragraph("Total").SetFont(boldFont)));

                foreach (var product in products)
                {
                    decimal lineTotal = product.Quantity * product.Price;

                    table.AddCell(new Cell().Add(new Paragraph(product.Name).SetFont(normalFont)));
                    table.AddCell(new Cell().Add(new Paragraph(product.Quantity.ToString()).SetFont(normalFont)));
                    table.AddCell(new Cell().Add(new Paragraph($"{product.Price:C}").SetFont(normalFont)));
                    table.AddCell(new Cell().Add(new Paragraph($"{lineTotal:C}").SetFont(normalFont)));
                }

                document.Add(table);

                // Total
                document.Add(new Paragraph($"\nTotal Amount: {totalAmount:C}")
                    .SetFont(boldFont)
                    .SetFontSize(12)
                    .SetTextAlignment(TextAlignment.RIGHT));

                // Footer
                document.Add(new Paragraph("\nThank you for your purchase!")
                    .SetFont(italicFont)
                    .SetTextAlignment(TextAlignment.CENTER)
                    .SetFontSize(14));

                document.Close();
                return memoryStream.ToArray();
            }
        }
    }
}
