from Read import ShoeReader

class ShoeOperations:
    @staticmethod
    def display_shoes(shoes, title="Shoes Inventory"):  
        if not shoes:
            print("No shoes available in inventory.")
            return
        
        print("\n" + "=" * 90)
        print("{:^90}".format(title))  
        print("=" * 90)
        print("{:<4} {:<20} {:<15} {:<10} {:<15} {:<15}".format(
            'No.', 'Type', 'Brand', 'Quantity', 'Price', 'Origin'
        ))
        print("-" * 90)
        
        for i, shoe in enumerate(shoes, 1):
            print("{:<4} {:<20} {:<15} {:<10} ${:<14.2f} {:<15}".format(
                i, 
                shoe['type'][:19],
                shoe['brand'][:14],
                shoe['quantity'], 
                shoe['price'], 
                shoe['origin'][:14]
            ))
        
        print("=" * 90)
        
        total_items = len(shoes)
        total_value = sum(shoe['quantity'] * shoe['price'] for shoe in shoes)
        total_quantity = sum(shoe['quantity'] for shoe in shoes)
        
        print("Summary: {} items, {} units, Total Value: ${:,.2f}".format(
            total_items, total_quantity, total_value
        ))
        print("=" * 90)

    @staticmethod
    def add_new_shoe():
        print("ADD NEW SHOE")
        
        try:
            shoe_type = input("Shoe type: ").strip()
            if not shoe_type:
                raise ValueError("Shoe type cannot be empty.")
            
            brand = input("Brand: ").strip()
            if not brand:
                raise ValueError("Brand cannot be empty.")
            
            quantity = int(input("Quantity: "))
            if quantity < 0:  
                raise ValueError("Quantity cannot be negative. Please enter 0 or positive number.")
            
            price = float(input("Price: $"))
            if price <= 0:
                raise ValueError("Price must be positive.")
            
            origin = input("Origin: ").strip()
            if not origin:
                raise ValueError("Origin cannot be empty.")
            
            return {
                'type': shoe_type,
                'brand': brand,
                'quantity': quantity,
                'price': price,
                'origin': origin
            }
            
        except ValueError as e:
            print("Input error: {}".format(e))
            return None

    @staticmethod
    def update_quantity(shoes):
        if not shoes:
            print("No shoes available to update.")
            return shoes
        
        ShoeOperations.display_shoes(shoes, "Select Shoe to Update")
        
        try:
            choice = int(input("\nEnter shoe number to update: "))
            if 1 <= choice <= len(shoes):
                new_qty = int(input("Enter new quantity: "))
                if new_qty < 0:
                    raise ValueError("Quantity cannot be negative.")
                
                shoes[choice-1]['quantity'] = new_qty
                print("Quantity updated successfully!")
            else:
                print("Invalid selection. Please choose a valid number.")
        except ValueError as e:
            print("Error: {}".format(e))
        
        return shoes

    @staticmethod
    def display_low_stock(shoes):
        low_stock = ShoeReader.find_lowest_quantity(shoes)
        if low_stock:
            ShoeOperations.display_shoes(low_stock, "LOW STOCK ITEMS (Need Restocking)")
        else:
            print("All items have sufficient stock.")

    @staticmethod
    def purchase_stock(shoes):
        print("\n" + "="*40)
        print("PURCHASE STOCK")
        print("="*40)
        
        purchase_items = []
        temp_shoes = shoes.copy()
        
        while True:
            print("\n1. Add to existing shoe")
            print("2. Add new shoe type")
            print("3. Finish purchase")
            choice = input("Choose option (1-3): ").strip()
            
            if choice == '3':
                break
                
            try:
                if choice == '1':
                    if not temp_shoes:
                        print("No shoes available. Please add new shoe first.")
                        continue
                        
                    ShoeOperations.display_shoes(temp_shoes, "Select Shoe to Restock")
                    shoe_choice = int(input("Enter shoe number: "))
                    
                    if 1 <= shoe_choice <= len(temp_shoes):
                        purchase_qty = int(input("Enter quantity to purchase: "))
                        if purchase_qty <= 0:
                            print("Quantity must be positive.")
                            continue
                        
                        unit_price = float(input("Enter unit purchase price: $"))
                        if unit_price <= 0:
                            print("Price must be positive.")
                            continue
                        
                        vat_percent = float(input("Enter VAT percentage (0 if none): "))
                        discount_percent = float(input("Enter discount percentage (0 if none): "))
                        
                        subtotal = purchase_qty * unit_price
                        discount_amount = subtotal * (discount_percent / 100)
                        amount_after_discount = subtotal - discount_amount
                        vat_amount = amount_after_discount * (vat_percent / 100)
                        total_amount = amount_after_discount + vat_amount
                        
                        purchase_item = {
                            'type': temp_shoes[shoe_choice-1]['type'],
                            'brand': temp_shoes[shoe_choice-1]['brand'],
                            'quantity': purchase_qty,
                            'unit_price': unit_price,
                            'subtotal': subtotal,
                            'discount_percent': discount_percent,
                            'discount_amount': discount_amount,
                            'vat_percent': vat_percent,
                            'vat_amount': vat_amount,
                            'total_amount': total_amount,
                            'action': 'restock'
                        }
                        purchase_items.append(purchase_item)
                        
                        temp_shoes[shoe_choice-1]['quantity'] += purchase_qty
                        
                        print("Added {} units of {} {}".format(
                            purchase_qty, temp_shoes[shoe_choice-1]['brand'], temp_shoes[shoe_choice-1]['type']
                        ))
                        print("Item Total: ${:.2f}".format(total_amount))
                
                elif choice == '2':
                    new_shoe = ShoeOperations.add_new_shoe()
                    if new_shoe:
                        temp_shoes.append(new_shoe)
                        print("New shoe added to purchase list!")
                        
                        purchase_item = {
                            'type': new_shoe['type'],
                            'brand': new_shoe['brand'],
                            'quantity': new_shoe['quantity'],
                            'unit_price': new_shoe['price'],
                            'subtotal': new_shoe['quantity'] * new_shoe['price'],
                            'discount_percent': 0,
                            'discount_amount': 0,
                            'vat_percent': 0,
                            'vat_amount': 0,
                            'total_amount': new_shoe['quantity'] * new_shoe['price'],
                            'action': 'new'
                        }
                        purchase_items.append(purchase_item)
            
            except ValueError as e:
                print("Input error: {}".format(e))
        
        return temp_shoes, purchase_items

    @staticmethod
    def sell_shoes(shoes):
        if not shoes:
            print("No shoes available to sell.")
            return shoes, []
        
        sold_items = []
        temp_shoes = shoes.copy()
        
        while True:
            ShoeOperations.display_shoes(temp_shoes, "Available Shoes for Sale")
            print("\nEnter 0 to finish sale")
            
            try:
                choice = int(input("\nEnter shoe number to sell: "))
                
                if choice == 0:
                    break
                    
                if 1 <= choice <= len(temp_shoes):
                    sell_qty = int(input("Enter quantity to sell: "))
                    
                    if sell_qty <= 0:
                        print("Quantity must be positive.")
                        continue
                    
                    if sell_qty > temp_shoes[choice-1]['quantity']:
                        print("Not enough stock! Only {} available.".format(temp_shoes[choice-1]['quantity']))
                        continue
                    
                    selling_price = float(input("Enter selling price per unit: $"))
                    if selling_price <= 0:
                        print("Price must be positive.")
                        continue
                    
                    
                    subtotal = sell_qty * selling_price
                    discount_percent = 0 
                    vat_percent = 13  
                    
                    
                    user_input = input("Press Enter to use defaults or enter custom values: ")
                    if user_input:
                        discount_percent = float(input("Enter custom discount: "))
                        vat_percent = float(input("Enter custom VAT: "))
                    
                    discount_amount = subtotal * (discount_percent / 100)
                    amount_after_discount = subtotal - discount_amount
                    vat_amount = amount_after_discount * (vat_percent / 100)
                    total_amount = amount_after_discount + vat_amount
                    
                    sold_item = {
                        'type': temp_shoes[choice-1]['type'],
                        'brand': temp_shoes[choice-1]['brand'],
                        'quantity': sell_qty,
                        'unit_price': selling_price,
                        'subtotal': subtotal,
                        'discount_percent': discount_percent,
                        'discount_amount': discount_amount,
                        'vat_percent': vat_percent,
                        'vat_amount': vat_amount,
                        'total_amount': total_amount
                    }
                    sold_items.append(sold_item)
                    
                    temp_shoes[choice-1]['quantity'] -= sell_qty
                    
                    print("Added {} × {} {}".format(
                        sell_qty, temp_shoes[choice-1]['brand'], temp_shoes[choice-1]['type']
                    ))
                    print("Item Total: ${:.2f}".format(total_amount))
                    
                else:
                    print("Invalid selection.")
                    
            except ValueError:
                print("Please enter valid numbers.")
        
        return temp_shoes, sold_items
