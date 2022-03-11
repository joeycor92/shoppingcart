from abc import ABC, abstractmethod
from typing import Dict

from shopping_cart_interface import IShoppingCart
from pricer import Pricer


class ShoppingCart(IShoppingCart):
    """
    Implementation of the shopping tills in our supermarket.
    """
    def __init__(self, price: Pricer):
        self.pricer = price
        self._contents: Dict[str, int] = {}
        self._contents_array = []
        # I have created an array here as when items are appended
        # to the array they are always put at the end. While I have made
        # this change, I believe that recently python 'dict' keeps the
        # order in which they are added so this is likely not needed.

    def add_item(self, item_type: str, number: int):
        # adds new item to or update existing item in the shopping cart
        try:
            int(number)
        except ValueError:
            print("The quantity must be a number.")
            return 0

        if item_type not in self.pricer.pricing_database:
            # checks if item is available for purchase by checking if it
            # is in the pricer. Returns 0 if not and leaves the function.
            print("Not available for purchase.")
            return 0

        if item_type not in self._contents:
            self._contents[item_type] = number
            self._contents_array.append(item_type)
            # if the item is not in the dictionary, then it is added to
            # both the dictionary and the array.
        else:
            self._contents[item_type] = self._contents[item_type] + number

    def remove_item(self, item_type: str, number: int):
        # removes existing item from the shopping cart

        if item_type not in self._contents_array:
            # checks if item is in the dictionary. If not then it cannot be
            # removed. So a message is returned to say that it is not in the cart.
            # The function is exited.
            print("Not currently in the shopping cart.")
            return 0

        if number >= self._contents[item_type]:
            self._contents.pop(item_type)
            self._contents_array.remove(item_type)
            # if the number that the user chooses to remove is greater than
            # or equal to the total quantity in the shopping cart, then it
            # is completely removed from both the dictionary and the array.
        else:
            self._contents[item_type] = self._contents[item_type] - number
            # if the number is less than the quantity in the shopping cart
            # then the number is subtracted from the quantity and the remaining
            # amount is the quantity still remaining in the cart.

    def print_receipt(self):
        total_amount = 0
        query = "In what order would you like to the receipt to be printed. Type the number and click enter.\n" \
                "1. Item Name\n" \
                "2. Quantity\n" \
                "3. Price\n"
        # query that will be printed, doesn't show up in the tests.
        options = [1, 2, 3]
        # there are only 3 options right now but could be expanded in the future.
        format_choice = []
        x = 0
        while x == 0:
            # a while loop which keeps going until the condition is satisfied
            # In this case, the condition is satisfied when the user enters a number
            # between 1 and 3.
            first_choice = int(input(query))
            if first_choice not in options:
                print("Please enter a number between 1 and 3.")
            else:
                format_choice.append(first_choice)
                # the number is added to the array
                x = 1
        while x == 1:
            second_choice = int(input())
            if second_choice not in options:
                # This checks to make sure that the user is entering a number
                # between 1 and 3.
                print("Please enter a number between 1 and 3.")
            else:
                if second_choice in format_choice:
                    # This checks that the number has not already been entered.
                    print("Already entered that number. Try again.\n")
                else:
                    format_choice.append(second_choice)
                    # Adds to the array. The condition that x=0 is now satisfied.
                    x = 0
        while x == 0:
            third_choice = int(input())
            if third_choice not in options:
                print("Please enter a number between 1 and 3.")
                # This checks to make sure that the user is entering a number
                # between 1 and 3.
            else:
                if third_choice in format_choice:
                    # This checks that the number has not already been entered.
                    print("Already entered that number. Try again.\n")
                else:
                    format_choice.append(third_choice)
                    # Adds to the array. The condition that x=1 is now satisfied.
                    x = 1

        for item in self._contents_array:
            price = self.pricer.get_price(item)
            # the price of the item is taken from the pricer_database.
            format_dict = {1: item, 2: self._contents[item], 3: price}
            # the dictionary is saved here. 1 relates to the item, 2 relates to the
            # quantity and 3 relates to the price of the item.
            total_amount += self.pricer.get_price(item)*self._contents[item]
            # the total amount is calculated here, it is the product of each item's price
            # multiplied by the item quantity. This is added on each time we iterate through
            # array.
            print(f"{format_dict[format_choice[0]]} - {format_dict[format_choice[1]]} - "
                  f"{format_dict[format_choice[2]]}")
            # This prints in the format that the user wants. For example format_choice[0]
            # could be 1 so it will take the dictionary entry for 1, which would be item,
            # which would mean that item is printed first.
        print(f"Total: {total_amount}")

class ShoppingCartCreator(ABC):
    """
    Interface for the ShoppingCart creator.
    The creation process will be delegated to the subclasses of this class.
    """
    @abstractmethod
    def factory_method(self) -> ShoppingCart:
        # return the ShoppingCart object
        pass

    def operation(self) -> ShoppingCart:
        # Here more operations can be performed on the ShoppingCart object
        # returns ShoppingCart object
        return self.factory_method()

class ShoppingCartConcreteCreator(ShoppingCartCreator):
    """
    Concrete class for the ShoppingCart creator.
    Implements the factory_method
    """
    def factory_method(self) -> ShoppingCart:
        # returns ShoppingCart object
        return ShoppingCart(Pricer())

