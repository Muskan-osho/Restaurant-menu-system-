class ShoeReader:
 @staticmethod
 def read_shoes_data(filename):
    shoes = []
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                try:
                    parts = line.strip().split(', ')
                    if len(parts) == 5:
                        quantity = int(parts[2])
                        if quantity < 0:  
                            print("Warning: Negative quantity found in line {}. Setting to 0.".format(line_num))
                            quantity = 0  
                        
                        shoe = {
                            'type': parts[0],
                            'brand': parts[1],
                            'quantity': quantity, 
                            'price': float(parts[3]),
                            'origin': parts[4]
                        }
                        shoes.append(shoe)
                except ValueError as e:
                    print("Error parsing line {}: {}".format(line_num, e))
                    continue
    except FileNotFoundError:
        raise Exception("Error: File '{}' not found.".format(filename))
    except Exception as e:
        raise Exception("Error reading file: {}".format(e))
    return shoes

 @staticmethod
 def search_shoes(shoes, search_term):  
        if not shoes or not search_term.strip():
            return []
        search_term = search_term.lower()
        results = []
        for shoe in shoes:
            if (search_term in shoe['type'].lower() or 
                search_term in shoe['brand'].lower()):
                results.append(shoe)
        return results

 @staticmethod
 def find_lowest_quantity(shoes):
        if not shoes:
            return []
        min_q = min(shoe['quantity'] for shoe in shoes)
        return [shoe for shoe in shoes if shoe['quantity'] == min_q]
