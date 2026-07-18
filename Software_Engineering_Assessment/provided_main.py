import coles
from datetime import datetime
import pandas as pd
from tabulate import tabulate

discounted_items = ['Shampoo', 'Juice', 'Apples', 'Bananas', 'Cake', 'Ice-cream']

def main(current_dateTime = datetime.now()):
    """
    This is the main system of the Coles checkout.
    """
    
    # Coles Online Shopping Store
    current_dateTime = datetime.now() if current_dateTime is None else current_dateTime
    print("Welcome to Coles Online Shopping Store (" + str(current_dateTime) + ")")

    current_day_name = current_dateTime.strftime('%A')

    is_valid_age = False

    while(not is_valid_age):
        try:
            age = int(input(">>> How old are you? \n"))

            is_valid_age = coles.is_age_valid(age)

            if not is_valid_age:
                print('The input age is invalid. The age must be integer with value from 1 to 120.')
        except:
            print('The input age is invalid. The age must be integer with value from 1 to 120.')
    
    shopping_cart = pd.DataFrame()
    product_list = pd.DataFrame.from_dict(coles.product_list,orient='index')

    while True: 
        # To buy something?
        to_buy = input(">>> Would you like to scan your products? (Yes, No) \n")
        if to_buy == "Yes":

            print(tabulate(product_list, tablefmt='pretty', headers=["NAME","PRICE"]))

            # Scan your products
            product_name = input(">>> Choose the product name from the list? \n")
            product_quantity = int(input(">>> How many items? \n"))

            if coles.is_input_valid(product_name, product_quantity):
                if coles.is_product_eligible(product_name, age, current_dateTime):

                    if not coles.is_product_overlimit(product_name, product_quantity, current_dateTime):

                        sub_total = coles.product_list[product_name]*int(product_quantity)
                  
                        new_item = {
                            "NAME": product_name,
                            "QUANTITY": product_quantity,
                            "SUBTOTAL": sub_total
                        }
                        shopping_cart = pd.concat([shopping_cart, pd.DataFrame([new_item])], ignore_index=True)
                        
                    else:
                        print("Sorry, each customer can purchase a limited number of items.")    
                else:
                    print("Sorry, you are not eligible to buy this product.")
            else:
                print("Your input is invalid. Please try again.")
        elif to_buy == "No":
            break

    if len(shopping_cart) <= 0:
        print('Your shopping cart is empty. The program will be terminated')
        exit(0)
    
    total_amount = shopping_cart['SUBTOTAL'].sum()


    # Calculate delivery charges
    distance_km = int(input(">>> This online store is for delivery only. Please input the delivery distance in kilometers. \n"))
    delivery_charges = coles.calculate_delivery_charges(distance_km, total_amount, current_day_name)
    new_item = {
        "NAME": 'DELIVERY CHARGES',
        "QUANTITY": '-',
        "SUBTOTAL": delivery_charges
    }
    shopping_cart = pd.concat([shopping_cart, pd.DataFrame([new_item])], ignore_index=True)
    
    
    # Apply discount of the day

    discount_list = []

    for idx, row in shopping_cart.iterrows():
        product_name = row['NAME']
        product_quantity = row['QUANTITY']

        if product_name in discounted_items:
            original_price = row['SUBTOTAL']
            
            discount = coles.discount_of_the_day(product_name, product_quantity, original_price, current_dateTime)

            if discount > 0:

                new_item = {
                    "NAME": 'DISCOUNT - {}'.format(product_name),
                    "QUANTITY": '-',
                    "SUBTOTAL": -discount
                }

                discount_list.append(new_item)

    discount_df = pd.DataFrame(discount_list)

    shopping_cart = pd.concat([shopping_cart, discount_df])

    # Calculate the total amount
    totalamount = shopping_cart['SUBTOTAL'].sum()
    new_item = {
        "NAME": 'TOTAL AMOUNT',
        "QUANTITY": '-',
        "SUBTOTAL": totalamount
    }
    shopping_cart = pd.concat([shopping_cart, pd.DataFrame([new_item])], ignore_index=True)
    
    
    # Print the receipt
    print(">>> Thank you for shopping at Coles")
    print(">>> Here is your receipt. ")
    print(tabulate(shopping_cart, headers='keys', tablefmt='pretty'))
    return totalamount

if __name__ == "__main__":
    main()