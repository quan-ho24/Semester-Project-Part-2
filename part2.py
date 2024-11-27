import datetime
# Read ManufacturerList.txt
def read_manufacturer_list(file_name):
    manufacturer_dict = {}
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            item_id = parts[0]
            manufacturer = parts[1]
            item_type = parts[2]
            damaged = parts[3] if len(parts) > 3 else None
            manufacturer_dict[item_id] = [manufacturer, item_type, damaged]
    print("Manufacturer List:", manufacturer_dict)
    return manufacturer_dict
# Read PriceList.txt
def read_price_list(file_name):
    price_dict = {}
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            item_id = parts[0]
            price = int(parts[1])
            price_dict[item_id] = price
    print("Price List:", price_dict)
    return price_dict
# Read ServiceDatesList.txt
def read_service_dates_list(file_name):
    service_date_dict = {}
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            item_id = parts[0]
            service_date = datetime.datetime.strptime(parts[1], '%m/%d/%Y').date()
            service_date_dict[item_id] = service_date
    print("Service Dates List:", service_date_dict)
    return service_date_dict
# Combine Data
def combine_data(manufacturer_dict, price_dict, service_date_dict):
    full_inventory = []
    for item_id, details in manufacturer_dict.items():
        manufacturer, item_type, damaged = details
        price = price_dict.get(item_id, None)
        service_date = service_date_dict.get(item_id, None)
        full_inventory.append([item_id, manufacturer, item_type, price, service_date, damaged])
    print("Full Inventory Combined Data:", full_inventory)
    return full_inventory
# Write FullInventory.txt
def write_full_inventory(full_inventory, file_name):
    full_inventory.sort(key=lambda x: x[1])  # Sort by manufacturer
    with open(file_name, 'w') as file:
        for item in full_inventory:
            file.write(','.join(map(str, item)) + '\n')
def main():
    manufacturer_dict = read_manufacturer_list('ManufacturerList.txt')
    price_dict = read_price_list('PriceList.txt')
    service_date_dict = read_service_dates_list('ServiceDatesList.txt')
    full_inventory = combine_data(manufacturer_dict, price_dict, service_date_dict)
    write_full_inventory(full_inventory, 'FullInventory.txt')
if __name__ == "__main__":
    main()
