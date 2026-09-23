using System;
using System.Globalization;

namespace PaymentService
{
    public class Class1
    {
        public static void Main(string[] args)
        {
            if(args.Length < 3)
            {
                Console.WriteLine("FAILED: Missing Arguments");
                return;
            }

            try
            {
                double basePrice = double.Parse(args[0], CultureInfo.InvariantCulture);
                int age = int.Parse(args[1]);
                double amountPaid = double.Parse(args[2], CultureInfo.InvariantCulture);

                if(age < 18)
                {
                    basePrice *= 0.90;
                }

                basePrice = Math.Round(basePrice, 2);
                amountPaid = Math.Round(amountPaid, 2);

                if(amountPaid >= basePrice)
                {
                    double change = Math.Round(amountPaid - basePrice, 2);
                    Console.WriteLine($"SUCCESS:{basePrice.ToString("F2", CultureInfo.InvariantCulture)}:{change.ToString("F2", CultureInfo.InvariantCulture)}");
                }

                else
                {
                    Console.WriteLine($"FAILED: Insufficient Payment (Owed: ${basePrice:F2}, Paid: ${amountPaid:F2})");
                }
            }

            catch(Exception ex)
            {
                Console.WriteLine($"FAILED: Exception - {ex.Message}");
            }
        }
    }
}