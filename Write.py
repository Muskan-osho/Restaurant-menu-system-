import datetime

class ShoeWriter:
    @staticmethod
    def save_shoes_data(filename, shoes):
        try:
            with open(filename, 'w') as file:
                for shoe in shoes:
                    file.write("{}, {}, {}, {}, {}\n".format(
                        shoe['type'], shoe['brand'], shoe['quantity'], 
                        shoe['price'], shoe['origin']
                    ))
            return True
        except PermissionError:
            raise Exception("Error: Permission denied to write to file.")
        except Exception as e:
            raise Exception("Error saving file: {}".format(e))

    @staticmethod
    def generate_purchase_receipt(purchase_items, supplier_name=""):
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            receipt_filename = "purchase_receipt_{}.txt".format(timestamp)
            
            grand_total = sum(item['total_amount'] for item in purchase_items)
            
            with open(receipt_filename, 'w') as file:
                file.write(" PURCHASE RECEIPT \n")
                file.write("=" * 60 + "\n")
                file.write("Date: {}\n".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                if supplier_name:
                    file.write("Supplier: {}\n".format(supplier_name))
                file.write("=" * 60 + "\n")
                
                for i, item in enumerate(purchase_items, 1):
                    file.write("Item {}: {} {}\n".format(i, item['brand'], item['type']))
                    file.write("Quantity: {} units\n".format(item['quantity']))
                    file.write("Unit Price: ${:.2f}\n".format(item['unit_price']))
                    file.write("Subtotal: ${:.2f}\n".format(item['subtotal']))
                    
                    if item['discount_percent'] > 0:
                        file.write("Discount ({:.1f}%): -${:.2f}\n".format(
                            item['discount_percent'], item['discount_amount']
                        ))
                    
                    if item['vat_percent'] > 0:
                        file.write("VAT ({:.1f}%): +${:.2f}\n".format(
                            item['vat_percent'], item['vat_amount']
                        ))
                    
                    file.write("Item Total: ${:.2f}\n".format(item['total_amount']))
                    file.write("-" * 60 + "\n")
                
                file.write("GRAND TOTAL: ${:.2f}\n".format(grand_total))
                file.write("=" * 60 + "\n")
            
            print(" Purchase receipt saved as '{}'".format(receipt_filename))
            return True
        except Exception as e:
            raise Exception("Error generating purchase receipt: {}".format(e))

    @staticmethod
    def generate_sales_receipt(sold_items, customer_name=""):
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            receipt_filename = "sales_receipt_{}.txt".format(timestamp)
            
            grand_total = sum(item['total_amount'] for item in sold_items)
            
            with open(receipt_filename, 'w') as file:
                file.write(" SALES RECEIPT \n")
                file.write("=" * 60 + "\n")
                file.write("Date: {}\n".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                if customer_name:
                    file.write("Customer: {}\n".format(customer_name))
                file.write("=" * 60 + "\n")
                
                for i, item in enumerate(sold_items, 1):
                    file.write("Item {}: {} {}\n".format(i, item['brand'], item['type']))
                    file.write("Qty: {} × ${:.2f} = ${:.2f}\n".format(
                        item['quantity'], item['unit_price'], item['subtotal']
                    ))
                    
                    if item['discount_percent'] > 0:
                        file.write("Discount ({:.1f}%): -${:.2f}\n".format(
                            item['discount_percent'], item['discount_amount']
                        ))
                    
                    if item['vat_percent'] > 0:
                        file.write("VAT ({:.1f}%): +${:.2f}\n".format(
                            item['vat_percent'], item['vat_amount']
                        ))
                    
                    file.write("Item Total: ${:.2f}\n".format(item['total_amount']))
                    file.write("-" * 60 + "\n")
                
                file.write("GRAND TOTAL: ${:.2f}\n".format(grand_total))
                file.write("=" * 60 + "\n")
                file.write("Thank you for your purchase!\n")
            
            print(" Sales receipt saved as '{}'".format(receipt_filename))
            return True
        except Exception as e:
            raise Exception("Error generating receipt: {}".format(e))

    @staticmethod
    def export_invoice(shoes, report_filename="inventory_invoice.txt"):
        try:
            with open(report_filename, 'w') as file:
                total_value = sum(shoe['quantity'] * shoe['price'] for shoe in shoes)
                
                file.write("=" * 90 + "\n")
                file.write("{:^90}\n".format("INVOICE - SHOES INVENTORY"))
                file.write("=" * 90 + "\n")
                file.write("{:<4} {:<20} {:<15} {:<10} {:<15} {:<15}\n".format(
                    'No.', 'Type', 'Brand', 'Quantity', 'Unit Price', 'Total Value'
                ))
                file.write("-" * 90 + "\n")
                
                for i, shoe in enumerate(shoes, 1):
                    item_value = shoe['quantity'] * shoe['price']
                    file.write("{:<4} {:<20} {:<15} {:<10} ${:<14.2f} ${:<14.2f}\n".format(
                        i, 
                        shoe['type'][:19],
                        shoe['brand'][:14],
                        shoe['quantity'], 
                        shoe['price'], 
                        item_value
                    ))
                
                file.write("=" * 90 + "\n")
                file.write("{:>70} ${:<18.2f}\n".format("GRAND TOTAL:", total_value))
                file.write("=" * 90 + "\n")
                file.write("Generated on: {}\n".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            print(" Invoice exported to '{}'".format(report_filename))
            return True
        except Exception as e:
            raise Exception("Error generating invoice: {}".format(e))

    @staticmethod
    def display_invoice(shoes):  
        if not shoes:
            print("No shoes available for invoice.")
            return
        
        total_value = sum(shoe['quantity'] * shoe['price'] for shoe in shoes)
        
        print("\n" + "=" * 90)
        print("{:^90}".format("INVOICE - SHOES INVENTORY"))
        print("=" * 90)
        print("{:<4} {:<20} {:<15} {:<10} {:<15} {:<15}".format(
            'No.', 'Type', 'Brand', 'Quantity', 'Unit Price', 'Total Value'
        ))
        print("-" * 90)
        
        for i, shoe in enumerate(shoes, 1):
            item_value = shoe['quantity'] * shoe['price']
            print("{:<4} {:<20} {:<15} {:<10} ${:<14.2f} ${:<14.2f}".format(
                i, 
                shoe['type'][:19],
                shoe['brand'][:14],
                shoe['quantity'], 
                shoe['price'], 
                item_value
            ))
        
        print("=" * 90)
        print("{:>70} ${:<18.2f}".format("GRAND TOTAL:", total_value))
        print("=" * 90)
