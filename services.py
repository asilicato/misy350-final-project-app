class InventoryService:
    def __init__(self, inventory):
        self.inventory = inventory

    def get_next_item_id(self):
        if len(self.inventory) == 0:
            return 1
        return max(item["item_id"] for item in self.inventory) + 1

    def get_item_by_name(self, item_name):
        for item in self.inventory:
            if item["name"] == item_name:
                return item
        return None

    def get_item_names(self):
        return [item["name"] for item in self.inventory]

    def get_low_stock_items(self):
        return [item for item in self.inventory if item["stock"] < 5]

    def get_inventory_value(self):
        total = 0
        for item in self.inventory:
            total += item["unit_price"] * item["stock"]
        return total