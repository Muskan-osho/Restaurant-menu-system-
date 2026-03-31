from Read import ShoeReader
from Write import ShoeWriter
from Operation import ShoeOperations

class ShoeInventorySystem:
    def __init__(self):
        self.shoes = []
        self.filename = "shoes.txt"
        self.shoe_reader = ShoeReader()
        self.shoe_writer = ShoeWriter()
        self.shoe_operations = ShoeOperations()         
    
    def load_data(self):
        try:
            self.shoes = ShoeReader.read_shoes_data(self.filename)
            print(" Loaded {} shoes from inventory.".format(len(self.shoes)))
        except Exception as e:
            print(e)
            self.initialize_sample_data()        
    
    def initialize_sample_data(self):
        print("Initializing with sample data. ")
        self.shoes = [
            {'type': 'Loafer Light', 'brand': 'GoldStar', 'quantity': 200, 'price': 1000, 'origin': 'domestic'},
            {'type': 'Inigo 732', 'brand': 'Caliber', 'quantity': 100, 'price': 2800, 'origin': 'domestic'},
            {'type': 'Lite Racer', 'brand': 'Adidas', 'quantity': 200, 'price': 7000, 'origin': 'international'}
        ]
        self.save_data()       
    
    def save_data(self):
        try:
            if ShoeWriter.save_shoes_data(self.filename, self.shoes):
                print(" Data saved successfully! ")
        except Exception as e:
            print(e)

    def search_shoes(self):
        term = input("\nEnter shoe type or brand to search: ").strip()
        if term:
            results = ShoeReader.search_shoes(self.shoes, term)  
            ShoeOperations.display_shoes(results, "Search Results for '{}'".format(term))
        else:
            print("Please enter a search term.")
    
    def show_transaction_summary(self, items, transaction_type):
       
        if not items:
            return
        
        total_amount = sum(item['total_amount'] for item in items)
        total_items = sum(item['quantity'] for item in items)
        
        print("\n{} SUMMARY:".format(transaction_type.upper()))
        
        print("Total Items: {}".format(total_items))
        print("Total Amount: ${:.2f}".format(total_amount))
        print("Items:")
        
        for i, item in enumerate(items, 1):
            print("  {}. {} {} - {} units - ${:.2f}".format(
                i, item['brand'], item['type'], item['quantity'], item['total_amount']
            ))
    
    def purchase_stock(self):
       
        updated_shoes, purchase_items = ShoeOperations.purchase_stock(self.shoes)
        
        if purchase_items:
            self.shoes = updated_shoes
            supplier = input("Enter supplier name (optional): ").strip()
            try:
                ShoeWriter.generate_purchase_receipt(purchase_items, supplier)
                
               
                self.show_transaction_summary(purchase_items, "purchase")
                
               
                total_amount = sum(item['total_amount'] for item in purchase_items)
                total_items = sum(item['quantity'] for item in purchase_items)
                print(" Purchase completed! {} items totaling ${:.2f}".format(total_items, total_amount))
                
            except Exception as e:
                print("Error generating receipt: {}".format(e))
        else:
            print("No items were purchased.")
    
    def sell_shoes(self):
      
        updated_shoes, sold_items = ShoeOperations.sell_shoes(self.shoes)
        
        if sold_items:
            self.shoes = updated_shoes
            customer = input("Enter customer name (optional): ").strip()
            try:
                ShoeWriter.generate_sales_receipt(sold_items, customer)
                
           
                self.show_transaction_summary(sold_items, "sale")
                
               
                total_amount = sum(item['total_amount'] for item in sold_items)
                total_items = sum(item['quantity'] for item in sold_items)
                print(" Sale completed! {} items sold for ${:.2f}".format(total_items, total_amount))
                
            except Exception as e:
                print("Error generating receipt: {}".format(e))
        else:
            print("No items were sold.")
    
    def display_menu(self):
        print("SHOE INVENTORY MANAGEMENT SYSTEM\n")
        
        print("1. View product")
        print("2. Add New Shoe")
        print("3. Search Shoes")
        print("4. Check Low Stock")
        print("5. Update Quantity")
        print("6. Purchase Stock")
        print("7. Sell Shoes")
        print("8. Generate Invoice")
        print("9. Save Data")
        print("10. Exit\n")
    
    def run(self):
        print(" Welcome to Shoe Inventory Management System ")
        self.load_data()
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice (1-10): ").strip()
                
                if choice == '1':
                    ShoeOperations.display_shoes(self.shoes)
                elif choice == '2':
                    new_shoe = ShoeOperations.add_new_shoe()
                    if new_shoe:
                        self.shoes.append(new_shoe)
                        print(" New shoe added to inventory ")
                elif choice == '3':
                    self.search_shoes()
                elif choice == '4':
                    low_stock = ShoeReader.find_lowest_quantity(self.shoes)
                    ShoeOperations.display_shoes(low_stock, " Low Stock Items ")
                elif choice == '5':
                    self.shoes = ShoeOperations.update_quantity(self.shoes)
                elif choice == '6':  
                    self.purchase_stock()
                elif choice == '7':  
                    self.sell_shoes()
                elif choice == '8':  
                    try:
                        ShoeWriter.display_invoice(self.shoes)
                        if ShoeWriter.export_invoice(self.shoes):
                            print(" Inventory invoice also saved to 'inventory_invoice.txt'\n")
                    except Exception as e:
                        print(e)
                elif choice == '9':  
                    self.save_data()
                elif choice == '10':  
                    save = input("Save changes before exiting? (yes/no): ").lower()
                    if save == 'yes':
                        self.save_data()
                    print("Thank you for using the system!")
                    break
                else:
                    print("Invalid choice! Please enter 1-10.")
            
            except KeyboardInterrupt:
                print("\n\nOperation cancelled.")
            except Exception as e:
                print("An error occurred: {}".format(e))

def main():
    system = ShoeInventorySystem()
    system.run()

if __name__ == "__main__":
    main()
