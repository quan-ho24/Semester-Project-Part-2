from datetime import datetime


class InventoryItem:
    """Represents a single item in the inventory."""
    def __init__(self, item_id, manufacturer, item_type, price, service_date, damaged):
        self.item_id = item_id
        self.manufacturer = manufacturer
        self.item_type = item_type
        self.price = price
        self.service_date = service_date
        self.damaged = damaged

    def __repr__(self):
        return f"{self.item_id},{self.manufacturer},{self.item_type},{self.price}," \
               f"{self.service_date.strftime('%m/%d/%Y')},{'damaged' if self.damaged else ''}"


class InventoryManager:
    """Manages the electronics store inventory."""
    def __init__(self):
        self.items = []

    def load_data(self, manufacturer_file, price_file, service_date_file):
        """Loads inventory data from text files."""
        manufacturer_dict = self._parse_manufacturer_list(manufacturer_file)
        price_dict = self._parse_price_list(price_file)
        service_date_dict = self._parse_service_dates(service_date_file)

        for item_id, details in manufacturer_dict.items():
            price = price_dict.get(item_id, 0.0)
            service_date = service_date_dict.get(item_id, datetime.today())
            damaged = details['damaged'] == 'damaged'
            item = InventoryItem(
                item_id=item_id,
                manufacturer=details['manufacturer'],
                item_type=details['item_type'],
                price=price,
                service_date=service_date,
                damaged=damaged
            )
            self.items.append(item)

    def _parse_manufacturer_list(self, file_name):
        """Reads and parses the ManufacturerList.txt file."""
        manufacturer_dict = {}
        with open(file_name, 'r') as file:
            for line in file:
                parts = [part.strip() for part in line.split(",")]  # Strip spaces around each part
                item_id = parts[0]
                manufacturer = parts[1]
                item_type = parts[2]
                damaged = parts[3].lower() if len(parts) > 3 else None
                manufacturer_dict[item_id] = {
                    'manufacturer': manufacturer,
                    'item_type': item_type,
                    'damaged': damaged
                }
        return manufacturer_dict

    def _parse_price_list(self, file_name):
        """Reads and parses the PriceList.txt file."""
        price_dict = {}
        with open(file_name, 'r') as file:
            for line in file:
                parts = [part.strip() for part in line.split(",")]
                item_id = parts[0]
                price = float(parts[1])
                price_dict[item_id] = price
        return price_dict

    def _parse_service_dates(self, file_name):
        """Reads and parses the ServiceDatesList.txt file."""
        service_date_dict = {}
        with open(file_name, 'r') as file:
            for line in file:
                parts = [part.strip() for part in line.split(",")]
                item_id = parts[0]
                service_date = datetime.strptime(parts[1], "%m/%d/%Y")
                service_date_dict[item_id] = service_date
        return service_date_dict

    def get_items_by_type_and_manufacturer(self, item_type=None, manufacturer=None):
        """Retrieve items based only on manufacturer and item type."""
        filtered_items = self.items  # Start with all items
        if item_type:
            filtered_items = [
                item for item in filtered_items if item.item_type.lower() == item_type.lower()
            ]
        if manufacturer:
            filtered_items = [
                item for item in filtered_items if item.manufacturer.lower() == manufacturer.lower()
            ]
        return filtered_items


class InteractiveQuery:
    """Handles user queries for inventory."""
    def __init__(self, inventory_manager):
        self.inventory_manager = inventory_manager

    def start(self):
        """Starts the interactive query loop."""
        print("Welcome to the Interactive Inventory Query System!")
        while True:
            query = input("Enter item manufacturer and type (or 'q' to quit): ").strip()
            if query.lower() == 'q':
                print("Goodbye!")
                break

            # Parse input into manufacturer and item type
            words = query.split()
            manufacturer = None
            item_type = None
            for word in words:
                for item in self.inventory_manager.items:
                    if word.lower() in item.manufacturer.lower():
                        manufacturer = word
                    if word.lower() in item.item_type.lower():
                        item_type = word

            if not manufacturer or not item_type:
                print("No such item in inventory")
                continue

            # Fetch matching items
            matching_items = self.inventory_manager.get_items_by_type_and_manufacturer(
                item_type=item_type, manufacturer=manufacturer
            )
            if not matching_items:
                print("No such item in inventory")
                continue

            # Display the first match
            matching_items.sort(key=lambda x: x.price, reverse=True)
            best_item = matching_items[0]
            print(f"Your item is: {best_item.item_id},{best_item.manufacturer},{best_item.item_type},{best_item.price}")

            # Optional: Display an alternative item if it exists
            alternative = self.find_closest_alternative(best_item)
            if alternative:
                print(f"You may also consider: {alternative.item_id},{alternative.manufacturer},{alternative.item_type},{alternative.price}")

    def find_closest_alternative(self, best_item):
        """Find an alternative item with the closest price from a different manufacturer."""
        alternatives = [
            item for item in self.inventory_manager.items
            if item.item_type == best_item.item_type and item.manufacturer != best_item.manufacturer
        ]
        if not alternatives:
            return None
        alternatives.sort(key=lambda x: abs(x.price - best_item.price))
        return alternatives[0] if alternatives else None


# Main function to run the program
def main():
    # Input file names
    manufacturer_file = "ManufacturerList.txt"
    price_file = "PriceList.txt"
    service_date_file = "ServiceDatesList.txt"

    # Load data into manager
    inventory_manager = InventoryManager()
    inventory_manager.load_data(manufacturer_file, price_file, service_date_file)

    # Start interactive query
    query_system = InteractiveQuery(inventory_manager)
    query_system.start()


if __name__ == "__main__":
    main()