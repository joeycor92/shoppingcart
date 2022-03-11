import unittest
from unittest import mock
from shopping_cart import ShoppingCartConcreteCreator
from test_utils import Capturing


class ShoppingCartTest(unittest.TestCase):

    @mock.patch('shopping_cart.input', clear=True)
    # mock patch included in a number of places to test the user input.
    def test_print_receipt(self, mocked_input):
        #Test to make sure that the receipt is printing correctly
        sc = ShoppingCartConcreteCreator().operation()
        mocked_input.side_effect = [2, 1, 3]
        # the user chooses to have the receipt printed as quantity - item type - price
        sc.add_item("apple", 2)
        with Capturing() as output:
            sc.print_receipt()
        self.assertEqual("2 - apple - 100", output[0])

    @mock.patch('shopping_cart.input', clear=True)
    def test_print_receipt_incorrect_input(self, mocked_input):
        #in this example the user initially puts in the incorrect input, 4, for the
        # third input and then puts in the correct input.
        sc = ShoppingCartConcreteCreator().operation()
        mocked_input.side_effect = [2, 1, 4, 3]
        sc.add_item("apple", 2)
        with Capturing() as output:
            sc.print_receipt()
        self.assertEqual("2 - apple - 100", output[1])

    @mock.patch('shopping_cart.input', clear=True)
    def test_string_not_number_for_quantity(self, mocked_input):
        #Test with an invalid second argument for add item.
        sc = ShoppingCartConcreteCreator().operation()
        mocked_input.side_effect = [2, 1, 3]
        with Capturing() as output:
            sc.add_item("apple", "x")
        self.assertEqual("The quantity must be a number.", output[0])

    @mock.patch('shopping_cart.input', clear=True)
    def test_remove_item_print_receipt(self, mocked_input):
        #Test for newly created remove item function. In this case the
        # user is first adding two apples and then removing one.
        sc = ShoppingCartConcreteCreator().operation()
        mocked_input.side_effect = [1, 2, 3]
        sc.add_item("apple", 2)
        sc.add_item("banana", 5)
        sc.remove_item("apple", 1)
        with Capturing() as output:
            sc.print_receipt()
        self.assertEqual("apple - 1 - 100", output[0])
        self.assertEqual("banana - 5 - 200", output[1])

    @mock.patch('shopping_cart.input', clear=True)
    def test_correct_total_print_receipt(self, mocked_input):
        #Prints the total value on the receipt.
        sc = ShoppingCartConcreteCreator().operation()
        mocked_input.side_effect = [1, 2, 3]
        sc.add_item("apple", 2)
        sc.add_item("banana", 5)
        with Capturing() as output:
            sc.print_receipt()
        self.assertEqual("apple - 2 - 100", output[0])
        self.assertEqual("banana - 5 - 200", output[1])
        self.assertEqual("Total: 1200")

    @mock.patch('shopping_cart.input', clear=True)
    def test_doesnt_explode_on_mystery_item(self, mocked_input):
        # Try to add pear or another item that is not in the pricer
        # which would mean that the product is not available.
        sc = ShoppingCartConcreteCreator().operation()
        mocked_input.side_effect = [1, 2, 3]

        with Capturing() as output:
            sc.add_item("apple", 2)
            sc.add_item("banana", 5)
            sc.add_item("pear", 5)
            sc.print_receipt()
        self.assertEqual("apple - 2 - 100", output[1])
        self.assertEqual("banana - 5 - 200", output[2])
        self.assertEqual("Not available for purchase.", output[0])


unittest.main(exit=False)
