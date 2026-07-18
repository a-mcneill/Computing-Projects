import math, datetime

product_list = {
    # Fresh Produce
    'Apples':2, 
    'Bananas':1, 
    'Eggs': 5,

    # Beverages
    'Water': 5, 
    'Juice': 4,

    # Household
    'Toilet paper': 4,
    'Shampoo': 5,
    'Cutting knife': 10,

    # Dessert
    'Ice-cream': 10, 
    'Cake': 20,
    
    # Liquor
    'Wine': 50,
    'Beer': 25,

    'Zero Alcohol': 20,
    'Cosmetic fillers': 20
}

liquor_list = ['Wine', 'Beer']

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
weekends = ['Saturday', 'Sunday']


def is_age_valid(age):
    """ 
    Function to determine if the user age input is valid.
    
    Age should be an integer greater than 0, and less than or equal to 120

    Args:
        age (int): 1 to 120

    Returns:
        True for valid age entered by user
        False for invalid age entered by user
    """
    
    # check that age is an integer, if not return False
    if not isinstance(age, int):
        return False
    
    # check if age is outside valid range (1 to 120 accepted), if not return True
    if age <= 0 or age > 120:
        return False

    # if age is int, age > 0 and <= 120, return True
    return True



def is_input_valid(product_name, product_quantity):
    """
    Function to determine if product name and product quantity are valid entries.

    Product name has to be in the product list, with case sensitivity, spelling, and spacing being an exact match.
    Product quantity should be at least one item.

    Args:
        product_name (str): a product from the product_list
        product_quantity (int): product quantity as available and greater than zero

    Returns:
        True for a valid product name and valid product quantity
        False for an invalid product name or invalid product quantity
    """
    
    # check that product name is a str, if not return False
    if not isinstance(product_name, str):
        return False

    # check that product quantity is an int, if not return False
    if not isinstance(product_quantity, int):
        return False

    # check that product name exists in the list and if the quantity is greater than zero
    if product_name not in product_list or product_quantity <= 0:
        return False

    # if product name is correct and quantity > 0, return True
    return True



def is_product_eligible(product_name, age, current_dateTime):
    """
    Function to determine if the product is eligible to be sold to the customer based on the product, stated age, and the date and time.

    The product name has to be in the product list and meet the requirements as passed through is_input_valid function.
    Age is the customer's entered age and is used to determine if the customer meets the legal requirements to purchase that product (e.g., alcohol, cutting knife, cosmetic fillers).
    current_dateTime is used to determine if the product (alcohol) can be sold based on the store manager's weekend and weekday alcohol trading periods.

    Args:
        product_name (str): a product from the product list
        age (int): customer's age to determine if they are eligible to purchase alcohol, cutting knife, or cosmetic fillers
        current_dateTime (datetime.datetime): the date and time of the attempted purchase

    Returns:
        True for a valid product, which the customer is eligible to purchase based on their age and the time
        False for an invalid product, or if the product is ineligible based on the customer's age or the time of attempted purchase
    """
    
    
    # get day name to determine if weekday or weekend as per weekday and weekend lists provided, as well as hour and minute to determine alcohol trading windows
    today_name = current_dateTime.strftime('%A')
    hour = current_dateTime.hour
    minute = current_dateTime.minute
    
    
    # check that customer is older than 15, if not, return False for the purchase of knife or comsetic fillers
    if product_name in ['Cutting knife', 'Cosmetic fillers'] and age < 15:
        return False

    
    # check if customer is under 18 years old, if so, return False for the purchase of alcohol regardless of time and date
    if product_name in liquor_list and age < 18:
        return False
    
    
    # check if 18 or older and apply weekday and weekend logic
    if product_name in liquor_list and age >= 18 :

        # check if weekday and apply 10 am to 3 pm alcohol trading window
        if today_name in weekdays:

            # check if time is before  10 am and after 3 pm, if so, return False
            if hour < 10 or (hour == 15 and minute > 0) or hour > 15:
                return False

        # check if weekend and apply 12 am to 4 am  and 10 pm to 11:59 pm alcohol trading window, if not in windows, return False
        if today_name in weekends:

            # define weekend window 1:
            wknd_window_1 = (hour < 4) or (hour == 4 and minute == 0)

            # define weekend window 2:
            wknd_window_2 = (hour >= 22)

            # if not in either window 1 (12 am to 4 am) or window 2 (10pm to 11:59 pm), return False
            if not (wknd_window_1 or wknd_window_2):
                return False


    # if customer >= 15 for knife and cosmetic fillers, or >= 18 and purchasing alcohol in the allowed windows, return True 
    # also returning true for products without age and time window restrictions
    return True


def is_product_overlimit(product_name, product_quantity, current_dateTime):
    """
    Function to determine if a product quantity is over the limit based on the daily, holiday, or trading period limits instated by the store manager.

    The product name is pulled through from the is is_input_valid and is_product_eligible functions.
    The product quantity is similarly pulled through from the is_input_valid function.
    current_dateTime is used to determine if the limits apply based on the date/holiday or time.

    Args:
        product_name (str): a product from the product list
        product_quantity (int): a product quantity as available and within respective limits and greater than zero
        current_dateTime (datetime.datetime): the date and time of the attempted purchase

    Returns:
        False for a product quantity that is not over the limit and is an eligible purchase
        True for a product quantity that is over the limit and has quantity restrictions
    """
    
    
    # get day name to determine if weekday or weekend, month, day, hour, and minute to determine if restrictions apply
    today_name = current_dateTime.strftime('%A')
    month = current_dateTime.month
    day = current_dateTime.day
    hour = current_dateTime.hour
    minute = current_dateTime.minute


    # apply toilet paper limit, no purchases > 2
    if product_name == 'Toilet paper' and product_quantity > 2:
        return True

    
    # apply christmas day and new year day liquor item restriction to no more than 4 per customer
    if ((day == 25 and month == 12) or (day == 1 and month == 1)) and product_name in liquor_list and product_quantity > 4:
        return True
    
    
    # apply weekday liquor items restrictions to two items per customer, except on christmas and new years day
    if today_name in weekdays and not ((day == 25 and month == 12) or (day == 1 and month == 1)):

        if product_name in liquor_list and product_quantity > 2:
            return True

    
    # apply ice-cream restriction from December to March to 3 items per customer
    if month in [12, 1, 2, 3] and product_name == 'Ice-cream' and product_quantity > 3:
        return True 
    
    
    # apply before 7pm restriction on Apples and Bananas, limited to 5 items per customer
    if product_name in ['Apples', 'Bananas'] and hour < 19 and product_quantity > 5:
        return True


    # apply June to July egg limit to 2 items per customer
    if month in [6, 7] and product_name == 'Eggs' and product_quantity > 2:
        return True
    
    # return False if product quantity not over applicable limits
    return False


def calculate_delivery_charges(distance_km, total_amount, current_day_name):
    """
    Function to calculate the delivery charges, taking into account the distance, total amount, and current day, in order to determine charge and if discount applies.

    distance is in kms and is rounded up as a kilometer (e.g., 340 meters becomes 1km)
    total amount is the total cost of the grocery shop
    current day is the day of order

    Args:
        distance_km (int): delivery distance rounded up as a kilometer integer
        total_amount (float): total cost of groceries in floating decimal format to two decimal places
        current_day_name (str): name of day of the week order is placed

    Returns:
        delivery charge (float) to two decimal places.
    """

    # get day to determine which discount applies if grocery cost >= $50 & normalise input convert datetime -> weekday string
    if isinstance(current_day_name, datetime.datetime):
        today_name =  current_day_name.strftime('%A')

    else:
        today_name = current_day_name

    
    # determine base delivery charge:

    # delivery charge if distance less than 3km
    if distance_km < 3:
        del_charge = 0

    # delivery charge if distance from 3 to 5km (inclusive)
    elif distance_km in [3, 4, 5]:
        del_charge = 2

    
    # delivery charge if distance is greater than 5km but less than or equal to 10km
    elif distance_km > 5 and distance_km <= 10:
        del_charge = ((distance_km - 5) * 1.5) + 2

    # delivery charge if distance is greater than 10km
    else:
        del_charge = 1.5 * distance_km


    # determine if weekday or weekend discount applies for spend >= $50:

    # weekday and cost greater than or equal to $50 - 10% discount
    if today_name in weekdays and distance_km > 5 and total_amount >= 50:
        del_charge = del_charge * 0.9
        
        # return the rounded delivery charge to two decimal places
        return round(del_charge, 2)

    
    # weekend and cost greater than or equal to $50 - 20% discount
    elif today_name in weekends and distance_km > 5 and total_amount >= 50:
        del_charge = del_charge * 0.8

        # return the rounded delivery charge to two decimal places
        return round(del_charge, 2)

    
    # return rounded delivery charge - including if spend < $50 and no delivery discount applies
    else:
        del_charge = round(del_charge, 2)
        return del_charge


    
    
def discount_of_the_day(product_name, product_quantity, original_price, current_dateTime):
    """
    Function to determine and apply discount of the day on applicable items, including shampoo in June and July, juice on weekends when multiples of three are purchased,
    fruit (apples and bananas) after 7pm, and on juice, cake, and ice-cream in December and January.

    The product name is pulled through from the is_input_valid and is_product_eligible functions
    The product quantity is similarly pulled through from the is_input_valid function
    original_price is the price of the item before discounts are applied
    current_dateTime is used to determine which discount, if any, apply.

    Args:
        product_name (str): a product from the product list
        product_quantity (int): a product quantity as available and within respective limits and greater than zero
        original_price (int): the price of the items (subtotal), used to determine discount value
        current_dateTime (datetime.datetime): the date and time of the attempted purchase

    Returns:
        discount amount (float): the amount that will be discounted from the subtotal to provide the final cost of groceries.
    """
    

    # get day name to determine if weekday or weekend, month, day, hour, and minute to determine the discount that applies, if any
    today_name = current_dateTime.strftime('%A')
    month = current_dateTime.month
    day = current_dateTime.day
    hour = current_dateTime.hour


    # discounts written as per priority order in order to ensure the correct discount is applied when any conflict
    
    # june and july shampoo 30% discount
    if month in [6,7] and product_name == "Shampoo":
        disc_amount = original_price * 0.3

    
    # weekend juice discount on every third bottle free
    elif today_name in weekends and product_name == "Juice":
        
        # buy two get the third bottle free - using unit price calc and free bottles calc to apply discount rate
        unit_price = original_price / product_quantity
        free_bottles = product_quantity // 3
        disc_amount = unit_price * free_bottles

    
    # weekday 7pm and later 50% fruit discount
    elif hour >= 19 and product_name in ["Apples", "Bananas"] and today_name in weekdays:
        disc_amount = original_price * 0.5

    
    # december and january 50% off juice, ice-cream, and cake
    elif month in [12, 1] and product_name in ["Juice", "Cake", "Ice-cream"]:
        disc_amount = original_price * 0.5

    # if none apply, no (0) discount
    else:
        disc_amount = 0


    # call & apply Australia day function discounts if applicable in addition to the discount of the day
    aus_disc_amount = discount_Australia_day(product_name, product_quantity, original_price, current_dateTime)

    # add Australia day discount to disc_amount
    disc_amount += aus_disc_amount
    
    
    # return discount amount - includes Aus day discount if applicable
    return disc_amount




def discount_Australia_day(product_name, product_quantity, original_price, current_dateTime):
    """
    Function to determine if any of the Australia day discounts apply to purchases made on Australia day.

    The five discount scenarios have been designed in the theme of Australian produce (Eggs, Apples, Bananas (assuming produced/grown in Australia),Wines (vineyards), and Beers (breweries)),
    as well as, promoting healthy snacks and alternatives - focusing the largest discounts on zero-alcohol options and on water, apples, and bananas.

    Five discount scenarios:
        1. Before 11 am, when a customer buys 2 or more eggs they recieve 40% off. Supports farmers and incentivises cooking breakfast/brunch at home.
        2. Before 3 pm, when a customer buys more than 3 wine items, they receive 60% off. Celebrating Australian vineyards.
        3. Before 3 pm, when a customer buys more than 2 beer items, they receive 50% off. Celebrating Australian breweries.
        4. Before 1 pm, when a customer buys more than 2 zero-alcohol items, they recieve 80% off. Promoting alcohol-free alternatives.
        5. Before 6 pm, when a customer buys water, apples, or bananas, they recieve 75% off. Promoting healthy choices and snacks.

    The discounts utilise all input arguments by applying limitations on the date and time period, the product names by only applying to specific products, the product quantity by only applying when a certain amount of products purchased,
    and utilising the original price to calculate the discount amount.


    Args:
        product_name (str): a product from the product list - discount applies to eggs, wine, beer, zero-alcohol, water, apples, and bananas.
        product_quantity (int): a product quantity as available, within respective discount rules/applications and greater than zero.
        original_price (int): the price of the items (subtotal), used to determine discount value
        current_dateTime (datetime.datetime): the date and time of the attempted purchase - for discounts to apply, must be Australia day and within time limitations.
    
    Returns:
        discount amount (float): the amount that will be discounted from the subtotal to provide the final cost of groceries.
    
    Implementation:
        The function first checks if it is Australia day (26th of January).
        The function then evaluates the five discount rules in priority order using if/elif/else statements.
        The default discount amount is set to 0 & if no discount rules apply returns 0.
        If a discount applies, the function returns the discount amount as a float.
    """
    

    # get month, day, and hour to ensure and implement date and time restrictions
    month = current_dateTime.month
    day = current_dateTime.day
    hour = current_dateTime.hour


    #**** discounts ****

    # apply outer if statement for day and month - must be 26th of January
    if day == 26 and month == 1:

        # set default Australia day discount amount to = 0
        aus_disc_amount = 0
        
        ## discount 1: 40% off of eggs when 2 or more egg items are purchased
        if product_name == 'Eggs' and product_quantity >= 2 and hour < 11:
            aus_disc_amount = original_price * 0.4

        
        # discount 2: 60% off of wine when more than 3 items are purchased before 3 pm
        elif product_name == 'Wine' and product_quantity > 3 and hour < 15:
            aus_disc_amount = original_price * 0.6

        
        # discount 3: 50% off beer when more than 2 items are purchased before 3 pm
        elif product_name == 'Beer' and product_quantity > 2 and hour < 15:
            aus_disc_amount = original_price * 0.5

        
        # discount 4: 80% off zero-alcohol items when more than 2 items are bought before 1 pm
        elif product_name == 'Zero Alcohol' and product_quantity > 2 and hour < 13:
            aus_disc_amount = original_price * 0.8


        # discount 5: 75% off water, apples, and bananas before 6 pm
        elif product_name in ['Water', 'Apples', 'Bananas'] and hour < 18:
            aus_disc_amount = original_price * 0.75

        return aus_disc_amount

    # if date and time is not 26th of January or discounts do not apply, discount amount = 0 
    else:
        aus_disc_amount = 0

    # return Aus day discount amount
    return aus_disc_amount

