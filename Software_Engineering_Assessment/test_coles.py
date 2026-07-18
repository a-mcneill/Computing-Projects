import coles
import unittest, datetime


class TestAgeValidity(unittest.TestCase):
    """
    class for testing the is_age_valid(age) Function.
    """

    # valid age test cases
    def test_age_valid_boundary1(self):
        """test that age is valid for boundary case greater than 0"""
        age_inpt = coles.is_age_valid(1)
        self.assertEqual(age_inpt, True)

    def test_age_valid_boundary2(self):
        """test that age is valid for boundary case equal to 120"""
        age_inpt = coles.is_age_valid(120)
        self.assertEqual(age_inpt, True)

    def test_age_valid_inrange(self):
        """test that age is valid for age in defined range"""
        age_inpt = coles.is_age_valid(27)
        self.assertEqual(age_inpt, True)

    
    # invalid age test cases
    def test_age_invalid_older(self):
        """ test that age is not valid when > 120"""
        age_inpt = coles.is_age_valid(145)
        self.assertEqual(age_inpt, False)

    def test_age_invalid_zero(self):
        """test that age is not valid when < 1"""
        age_inpt = coles.is_age_valid(0)
        self.assertEqual(age_inpt, False)

    def test_age_invalid_float(self):
        """test that age is not valid when entered as a decimal"""
        age_inpt = coles.is_age_valid(14.5)
        self.assertEqual(age_inpt, False)

    def test_age_invalid_str(self):
        """test that age is not valid when entered as a string"""
        age_inpt = coles.is_age_valid('twenty one')
        self.assertEqual(age_inpt, False)



class TestInputValid(unittest.TestCase):
    """
    class to test is_input_valid(product_name, product_quantity) Function
    """

    # valid name test cases
    def test_product_name_valid_in_list(self):
        """test that product name entered is in list"""
        product_inpt = coles.is_input_valid('Apples', 2)
        self.assertEqual(product_inpt, True)

    def test_product_name_invalid_not_in_list(self):
        """test that product name is not valid when not in product list"""
        product_inpt = coles.is_input_valid('Mango', 4)
        self.assertEqual(product_inpt, False)

    def test_product_name_invalid_casing(self):
        """test that product name is not valid when case sensitivity is not followed"""
        product_inpt = coles.is_input_valid('apples', 1)
        self.assertEqual(product_inpt, False)

    def test_product_name_invalid_int_entry(self):
        """test that product name is not valid when an int rather than str is entered"""
        product_inpt = coles.is_input_valid(12, 2)
        self.assertEqual(product_inpt, False)

    
    # valid quantity test cases
    def test_product_quant_valid(self):
        """test that product quantity is valid when both product in list and quantity available"""
        product_inpt = coles.is_input_valid('Ice-cream', 4)
        self.assertEqual(product_inpt, True)

    def test_product_quant_invalid_float(self):
        """test that product quantity is invalid when a float rather than integer"""
        product_inpt = coles.is_input_valid('Wine', 1.5)
        self.assertEqual(product_inpt, False)

    def test_product_quant_invalid_str(self):
        """test that product quantity is invalid when entered as a string"""
        product_inpt = coles.is_input_valid('Shampoo', 'one')
        self.assertEqual(product_inpt, False)

    def test_product_quant_invalid_zero(self):
        """test that product quantity is invalid when less than one"""
        product_inpt = coles.is_input_valid('Juice', 0)
        self.assertEqual(product_inpt, False)



class TestProductEligible(unittest.TestCase):
    """
    class to test if a product is eligible based upon the product, age of cumstomer, and the current date and time
    """

    # weekday alcohol test cases
    def test_eligible_product_alcohol_18_weekday_10(self):
        """test that customer who is 18 can purchase liquor at 10 am on a weekday"""
        dt = datetime.datetime(2026, 4, 9, 10, 0)    # 10:00 am, 09/04/2026
        prod_purch = coles.is_product_eligible('Beer', 18, dt)
        self.assertEqual(prod_purch, True)

    def test_eligible_product_alcohol_over18_weekday_15(self):
        """test that customer who is older than 18 can purchase liquor at 3 pm on a weekday"""
        dt = datetime.datetime(2026, 4, 9, 15, 0)    # 3:00 pm, 09/04/2026
        prod_purch = coles.is_product_eligible('Wine', 31, dt)
        self.assertEqual(prod_purch, True)

    def test_ineligible_product_alcohol_over18_weekday_959(self):
        """test that customer over 18 cannot purchase liquor on a weekday before 10 am"""
        dt = datetime.datetime(2026, 4, 10, 9, 59)  # 9:59 am, 10/04/2026
        prod_purch = coles.is_product_eligible('Beer', 61, dt)
        self.assertEqual(prod_purch, False)
    
    def test_ineligible_product_alcohol_over18_weekday_15(self):
        """test that customer over 18 cannot purchase liquor on a weekday after 3 pm"""
        dt = datetime.datetime(2026, 4, 10, 15, 1)  # 3:01 pm, 10/04/2026
        prod_purch = coles.is_product_eligible('Beer', 45, dt)
        self.assertEqual(prod_purch, False)


    # weekend alcohol test cases
    def test_eligible_product_alcohol_over18_weekend_midnight(self):
        """test that customer who is over 18 can purchase liquor at 12 am on a weekend"""
        dt = datetime.datetime(2026, 4, 11, 0, 0)   # 12:00 am, 11/04/2026
        prod_purch = coles.is_product_eligible('Wine', 22, dt)
        self.assertEqual(prod_purch, True)
    
    def test_eligible_product_alcohol_18_weekend_4(self):
        """test that customer who is 18 can purchase liquor at 4 am on a weekend"""
        dt = datetime.datetime(2026, 4, 11, 4, 0)   # 4:00 am, 11/04/2026
        prod_purch = coles.is_product_eligible('Wine', 18, dt)
        self.assertEqual(prod_purch, True)

    def test_eligible_product_alcohol_over18_weekend_22(self):
        """test that customer who is over 18 can purchase liquor at 10 pm on a weekend"""
        dt = datetime.datetime(2026, 4, 11, 22, 0)   # 10:00 pm, 11/04/2026
        prod_purch = coles.is_product_eligible('Beer', 26, dt)
        self.assertEqual(prod_purch, True)

    def test_ineligible_product_alcohol_over18_weekend_401(self):
        """test that customer who is over 18 cannot pruchase alcohol past 4 am on a weekend"""
        dt = datetime.datetime(2026, 4, 11, 4, 1)   # 04:01 am, 11/04/2026
        prod_purch = coles.is_product_eligible('Wine', 30, dt)
        self.assertEqual(prod_purch, False)

    def test_ineligible_product_alcohol_over18_weekend_959(self):
        """test that customer who is over 18 cannot pruchase alcohol before 10 pm on a weekend"""
        dt = datetime.datetime(2026, 4, 11, 21, 59)   # 9:59 pm, 11/04/2026
        prod_purch = coles.is_product_eligible('Beer', 55, dt)
        self.assertEqual(prod_purch, False)

    def test_ineligible_product_alcohol_u18(self):
        """test that a customer who is under 18 cannot purchase alcohol"""
        dt = datetime.datetime(2026, 4, 12, 22, 30) # 10:30 pm, 12/04/2026
        prod_purch = coles.is_product_eligible('Beer', 16, dt)
        self.assertEqual(prod_purch, False)


    # cosmetic fillers and knife 15 yrs test cases
    def test_eligible_product_cosmetic_15(self):
        """test that a customer who is 15 can purchase cosmetic fillers"""
        dt = datetime.datetime(2026, 4, 5, 11, 25)  # 11:25 am, 05/04/2026
        prod_purch = coles.is_product_eligible('Cosmetic fillers', 15, dt)
        self.assertEqual(prod_purch, True)

    def test_ineligible_product_cosmetic_u15(self):
        """test that a customer who is under 15 cannot purchase cosmetic fillers"""
        dt = datetime.datetime(2026, 4, 7, 10, 45)  # 10:45 am, 07/04/2026
        prod_purch = coles.is_product_eligible('Cosmetic fillers', 14, dt)
        self.assertEqual(prod_purch, False)

    def test_eligible_product_knife_15(self):
        """test that a customer who is 15 can purchase a cutting knife"""
        dt = datetime.datetime(2026, 4, 21, 14, 2)  # 2:02 pm, 21/04/2026
        prod_purch = coles.is_product_eligible('Cutting knife', 15, dt)
        self.assertEqual(prod_purch, True)

    def test_ineligible_product_knife_u15(self):
        """test that a customer who is under 15 cannot purchase a cutting knife"""
        dt = datetime.datetime(2026, 4, 24, 18, 5)  # 6:05 pm, 24/04/2026
        prod_purch = coles.is_product_eligible('Cutting knife', 14, dt)
        self.assertEqual(prod_purch, False)


    # general non-age restricted product test cases
    def test_eligible_product_nonalcohol_1(self):
        """test that general, non age-restricted groceries can be purchased at any time by any age"""
        dt = datetime.datetime(2026, 5, 1, 12, 7)  # 12:07 pm, 01/05/2026
        prod_purch = coles.is_product_eligible('Cake', 12, dt)
        self.assertEqual(prod_purch, True)
    
    def test_eligible_product_nonalcohol_2(self):
        """test that general, non age-restricted groceries can be purchased at any time by any age"""
        dt = datetime.datetime(2026, 4, 4, 9, 45)  # 09:45 am, 04/04/2026
        prod_purch = coles.is_product_eligible('Ice-cream', 9, dt)
        self.assertEqual(prod_purch, True)

    

class TestProductOverLimit(unittest.TestCase):
    """
    class for testing the is_product_overlimit Function. False if not over limit and True if over limit.
    """

    # toilet paper test cases
    def test_product_withinlimit_toiletpaper(self):
        """test that customer can purchase up to 2 toilet paper on any day"""
        dt = datetime.datetime(2026, 4, 14, 8, 47)  # 8:47 am, 14/04/2026
        prod_purch = coles.is_product_overlimit('Toilet paper', 2, dt)
        self.assertEqual(prod_purch, False)

    def test_product_overlimit_toiletpaper(self):
        """test that customer cannot purchase more than 2 toilet paper on any day"""
        dt = datetime.datetime(2026, 4, 11, 10, 47)  # 10:47 am, 11/04/2026
        prod_purch = coles.is_product_overlimit('Toilet paper', 3, dt)
        self.assertEqual(prod_purch, True)

    
    # alcohol test cases
    def test_product_weekday_withinlimit_alcohol(self):
        """test that a customer can purchase up to 2 alcohol items on a weekday"""
        dt = datetime.datetime(2026, 4, 15, 18, 24) # 6:24 pm, 15/04/2026
        prod_purch = coles.is_product_overlimit('Wine', 2, dt)
        self.assertEqual(prod_purch, False)

    def test_product_weekday_overlimit_alcohol(self):
        """test that a customer cannot purchase more than 2 alcohol items on a weekday"""
        dt = datetime.datetime(2026, 4, 14, 13, 58) # 1:58 pm, 14/04/2026
        prod_purch = coles.is_product_overlimit('Beer', 4, dt)
        self.assertEqual(prod_purch, True)

    def test_product_weekend_nolimit_alcohol(self):
        """test that a customer can purchase alcohol items on a weekend with no restrictions"""
        dt = datetime.datetime(2026, 4, 18, 19, 13) # 7:13 pm, 18/04/2026
        prod_purch = coles.is_product_overlimit('Wine', 7, dt)
        self.assertEqual(prod_purch, False)


    def test_product_xmas_withinlimit_alcohol(self):
        """test that a customer can purchase up to 4 alcohol items on christmas day"""
        dt = datetime.datetime(2026, 12, 25, 13, 58) # 1:58 pm, 25/12/2026
        prod_purch = coles.is_product_overlimit('Beer', 4, dt)
        self.assertEqual(prod_purch, False)

    def test_product_nyd_withinlimit_alcohol(self):
        """test that a customer can purchase up to 4 alcohol items on new years day"""
        dt = datetime.datetime(2027, 1, 1, 13, 58) # 1:58 pm, 01/01/2027
        prod_purch = coles.is_product_overlimit('Wine', 4, dt)
        self.assertEqual(prod_purch, False)

    def test_product_xmas_overlimit_alcohol(self):
        """test that a customer cannot purchase more than 4 alcohol items on christmas day"""
        dt = datetime.datetime(2026, 12, 25, 13, 58) # 1:58 pm, 25/12/2026
        prod_purch = coles.is_product_overlimit('Beer', 6, dt)
        self.assertEqual(prod_purch, True)

    def test_product_nyd_overlimit_alcohol(self):
        """test that a customer cannot purchase more than 4 alcohol items on new years day"""
        dt = datetime.datetime(2027, 1, 1, 13, 58) # 1:58 pm, 01/01/2027
        prod_purch = coles.is_product_overlimit('Wine', 5, dt)
        self.assertEqual(prod_purch, True)

    # test non-liquor cases on xmas and NY days
    def test_product_xmas_nolimit_nonliquor(self):
        """test that a customer can purchase non-alcohol items on christmas day without restriction"""
        dt = datetime.datetime(2026, 12, 25, 13, 58) # 1:58 pm, 25/12/2026
        prod_purch = coles.is_product_overlimit('Zero Alcohol', 5, dt)
        self.assertEqual(prod_purch, False)

    def test_product_nyd_nolimit_nonliquor(self):
        """test that a customer can purchase non-alcohol items on new years day without restriction"""
        dt = datetime.datetime(2027, 1, 1, 13, 58) # 1:58 pm, 01/01/2027
        prod_purch = coles.is_product_overlimit('Zero Alcohol', 7, dt)
        self.assertEqual(prod_purch, False)

    def test_product_xmas_nolimit_nonliquor_juice(self):
        """test that a customer can purchase non-alcohol items on christmas day without restriction"""
        dt = datetime.datetime(2026, 12, 25, 14, 50) # 2:50 pm, 25/12/2026
        prod_purch = coles.is_product_overlimit('Juice', 3, dt)
        self.assertEqual(prod_purch, False)

    def test_product_nyd_nolimit_nonliquor_water(self):
        """test that a customer can purchase non-alcohol items on new years day without restriction"""
        dt = datetime.datetime(2027, 1, 1, 11, 49) # 11:49 pm, 01/01/2027
        prod_purch = coles.is_product_overlimit('Water', 7, dt)
        self.assertEqual(prod_purch, False)

    
    # ice-cream test cases
    def test_icecream_withinlimit_decmarch(self):
        """test that a customer can purchase up to 3 ice-cream items during Dec-March trading period"""
        dt = datetime.datetime(2026, 12, 12, 15, 23) # 3:23 pm, 12/12/2026
        prod_purch = coles.is_product_overlimit('Ice-cream', 3, dt)
        self.assertEqual(prod_purch, False)

    def test_icecream_overlimit_decmarch(self):
        """test that a customer cannot purchase more than 3 ice-cream items during Dec-March trading period"""
        dt = datetime.datetime(2027, 2, 28, 12, 23) # 12:23 pm, 28/2/2027
        prod_purch = coles.is_product_overlimit('Ice-cream', 5, dt)
        self.assertEqual(prod_purch, True)


    def test_icecream_withinlimit_aprnov(self):
        """test that a customer can purchase ice-cream items without restriction during Apr-Nov trading period"""
        dt = datetime.datetime(2026, 4, 15, 16, 1) # 4:01 pm, 15/04/2026
        prod_purch = coles.is_product_overlimit('Ice-cream', 8, dt)
        self.assertEqual(prod_purch, False)


    # bananas and apples test cases
    def test_bananas_after_7pm(self):
        """test that bananas are not limited to 5 items per customer after 7pm"""
        dt = datetime.datetime(2026, 4, 15, 19, 1) # 7:01 pm, 15/04/2026
        prod_purch = coles.is_product_overlimit('Bananas', 8, dt)
        self.assertEqual(prod_purch, False)

    def test_bananas_before_7pm(self):
        """test that bananas are limited to 5 items per customer before 7pm"""
        dt = datetime.datetime(2026, 4, 15, 18, 59) # 6:59 pm, 15/04/2026
        prod_purch = coles.is_product_overlimit('Bananas', 6, dt)
        self.assertEqual(prod_purch, True)

    def test_apples_after_7pm(self):
        """test that apples are not limited to 5 items per customer after 7pm"""
        dt = datetime.datetime(2026, 4, 15, 19, 1) # 7:01 pm, 15/04/2026
        prod_purch = coles.is_product_overlimit('Apples', 10, dt)
        self.assertEqual(prod_purch, False)

    def test_apples_before_7pm(self):
        """test that apples are limited to 5 items per customer before 7pm"""
        dt = datetime.datetime(2026, 4, 22, 13, 50) # 1:50 pm, 22/04/2026
        prod_purch = coles.is_product_overlimit('Apples', 6, dt)
        self.assertEqual(prod_purch, True)


    # Eggs test cases
    def test_eggs_withinlimit_junjuly(self):
        """test that customers can purchase up to 2 egg items in June-July trading period"""
        dt = datetime.datetime(2026, 6, 1, 11, 5) # 11:05 am, 1/06/2026
        prod_purch = coles.is_product_overlimit('Eggs', 2, dt)
        self.assertEqual(prod_purch, False)

    def test_eggs_overlimit_junjuly(self):
        """test that customers cannot purchase more than 2 egg items in June-July trading period"""
        dt = datetime.datetime(2026, 6, 30, 9, 5) # 9:05 am, 30/06/2026
        prod_purch = coles.is_product_overlimit('Eggs', 3, dt)
        self.assertEqual(prod_purch, True)

    def test_eggs_withinlimit_augmay(self):
        """test that customers can purchase more than 2 egg items in August-May trading period"""
        dt = datetime.datetime(2026, 8, 17, 7, 15) # 7:15 am, 17/08/2026
        prod_purch = coles.is_product_overlimit('Eggs', 4, dt)
        self.assertEqual(prod_purch, False)



class TestCalcDeliveryCharges(unittest.TestCase):
    """
    class for testing the calculate_delivery_charges Function.
    """

    # delivery distance < 3km - no charge
    def test_under_3km_nocharge(self):
        """test that there is no charge for delivery distance less than 3km"""
        dt = datetime.datetime(2026, 4, 15, 20, 41)
        del_cost = coles.calculate_delivery_charges(2, 10, dt)
        self.assertEqual(del_cost, 0)


    # delivery distance 3 to 5 km
    def test_3to5km_charge3km(self):
        """test that the charge is $2 if the delivery distance is 3 to 5 kms"""
        dt = datetime.datetime(2026, 4, 15, 20, 41)
        del_cost = coles.calculate_delivery_charges(3, 10, dt)
        self.assertEqual(del_cost, 2)

    def test_3to5km_charge5km(self):
        """test that the charge is $2 if the delivery distance is 3 to 5 kms"""
        dt = datetime.datetime(2026, 4, 15, 20, 41)
        del_cost = coles.calculate_delivery_charges(5, 10, dt)
        self.assertEqual(del_cost, 2)


    # delivery distance is from 5 to 10km
    def test_5to10km_charge6km(self):
        """test that the charge is $2 + $1.5/km if the delivery distance is 5 to 10 kms"""
        dt = datetime.datetime(2026, 4, 12, 12, 41)
        del_cost = coles.calculate_delivery_charges(6, 10, dt)
        self.assertEqual(del_cost, 3.5)

    def test_5to10km_charge8km(self):
        """test that the charge is $2 + $1.5/km if the delivery distance is 5 to 10 kms"""
        dt = datetime.datetime(2026, 4, 12, 15, 41)
        del_cost = coles.calculate_delivery_charges(8, 10, dt)
        self.assertEqual(del_cost, 6.5)

    def test_5to10km_charge10km(self):
        """test that the charge is $2 + $1.5/km if the delivery distance is 5 to 10 kms"""
        dt = datetime.datetime(2026, 4, 12, 15, 41)
        del_cost = coles.calculate_delivery_charges(10, 10, dt)
        self.assertEqual(del_cost, 9.5)


    # delivery distance > 10 kms
    def test_10km_charge(self):
        """test that the charge is $1.5/km if the delivery distance is greater than 10 kms"""
        dt = datetime.datetime(2026, 5, 1, 11, 22)
        del_cost = coles.calculate_delivery_charges(11, 10, dt)
        self.assertEqual(del_cost, 16.5)


    def test_15km_charge(self):
        """test that the charge is $1.5/km if the delivery distance is greater than 10 kms"""
        dt = datetime.datetime(2026, 5, 1, 11, 22)
        del_cost = coles.calculate_delivery_charges(15, 10, dt)
        self.assertEqual(del_cost, 22.5)

    
    # delivery distance > 5km & total price >= $50 - weekday
    def test_7km_charge_discount_wkday(self):
        """test that the charge is $2 + $1.5/km if the delivery distance is 5 to 10km + 10% weekday discount on spend >= $50"""
        dt = datetime.datetime(2026, 4, 15, 10, 22)
        del_cost = coles.calculate_delivery_charges(7, 50, dt)
        self.assertEqual(del_cost, 4.5)

    
    def test_12km_charge_discount_wkday(self):
        """test that the charge is $1.5/km for the delivery distance is greater than 10km + 10% weekday discount on spend >= $50"""
        dt = datetime.datetime(2026, 4, 15, 10, 22)
        del_cost = coles.calculate_delivery_charges(12, 75, dt)
        self.assertEqual(del_cost, 16.2)


    # delivery distance > 5km & total price >= $50 - weekend
    def test_7km_charge_discount_wkend(self):
        """test that the charge is $2 + $1.5/km if the delivery distance is 5 to 10km + 20% weekend discount on spend >= $50"""
        dt = datetime.datetime(2026, 4, 19, 14, 22)
        del_cost = coles.calculate_delivery_charges(7, 50, dt)
        self.assertEqual(del_cost, 4)

    def test_12km_charge_discount_wkend(self):
        """test that the charge is $1.5/km for the delivery distance is greater than 10km + 20% weekend discount on spend >= $50"""
        dt = datetime.datetime(2026, 4, 18, 17, 12)
        del_cost = coles.calculate_delivery_charges(12, 100, dt)
        self.assertEqual(del_cost, 14.4)


    # additional test of current_day_name as string
    def test_1km_nocharge_string_currentday(self):
        """test that code works passing current_day_name as string"""
        self.assertEqual(coles.calculate_delivery_charges(1, 15, 'Wednesday'), 0)



class TestDiscountOfDay(unittest.TestCase):
    """
    class for testing the discount_of_the_day function.
    """

    # june to july Shampoo discount - 30%
    def test_discount_of_day_jun_shampoo_30(self):
        """test that shampoo bought in June has a 30% discount applied"""
        dt = datetime.datetime(2026, 6, 1, 10, 57)
        disc_items = coles.discount_of_the_day('Shampoo', 1, 5, dt)
        self.assertEqual(disc_items, 1.5)

    def test_discount_of_day_jul_shampoo_30(self):
        """test that shampoo bought in July has a 30% discount applied"""
        dt = datetime.datetime(2026, 7, 30, 16, 57)
        disc_items = coles.discount_of_the_day('Shampoo', 2, 10, dt)
        self.assertEqual(disc_items, 3)

    def test_discount_of_day_sep_shampoo_0(self):
        """test that shampoo bought outside of June & July has no discount applied"""
        dt = datetime.datetime(2026, 9, 28, 11, 0)
        disc_items = coles.discount_of_the_day('Shampoo', 1, 5, dt)
        self.assertEqual(disc_items, 0)


    # weekend buy 2 get 1 free juice
    def test_discount_of_day_wkend_juice_3(self):
        """test that when a customer buys three juices on a weekend, the third is free"""
        dt = datetime.datetime(2026, 4, 18, 12, 1)
        disc_items = coles.discount_of_the_day('Juice', 3, 12, dt)
        self.assertEqual(disc_items, 4)

    def test_discount_of_day_wkend_juice_6(self):
        """test that when a customer buys six juices on a weekend, the third and sixth is free"""
        dt = datetime.datetime(2026, 4, 18, 12, 1)
        disc_items = coles.discount_of_the_day('Juice', 6, 24, dt)
        self.assertEqual(disc_items, 8)

    def test_discount_of_day_wkend_juice_2(self):
        """test that when a customer buys two juices on a weekend, no discount"""
        dt = datetime.datetime(2026, 4, 19, 12, 1)
        disc_items = coles.discount_of_the_day('Juice', 2, 8, dt)
        self.assertEqual(disc_items, 0)

    def test_discount_of_day_wkday_juice_3(self):
        """test that when a customer buys three juices on a weekday, no discount applies"""
        dt = datetime.datetime(2026, 4, 16, 16, 1)
        disc_items = coles.discount_of_the_day('Juice', 3, 12, dt)
        self.assertEqual(disc_items, 0)


    # from 7pm weekday fruit discount - 50%
    def test_discount_of_day_wkday_7pm_apples_50(self):
        """test that when fruit (apples) is bought at 7pm on a weekday, 50% discount applies"""
        dt = datetime.datetime(2026, 4, 17, 19, 0)
        disc_items = coles.discount_of_the_day('Apples', 4, 8, dt)
        self.assertEqual(disc_items, 4)

    def test_discount_of_day_wkday_after7pm_bananas_50(self):
        """test that when fruit (bananas) is bought at 7pm on a weekday, 50% discount applies"""
        dt = datetime.datetime(2026, 4, 17, 21, 40)
        disc_items = coles.discount_of_the_day('Bananas', 3, 3, dt)
        self.assertEqual(disc_items, 1.5)

    def test_discount_of_day_wkday_before7pm_apples_0(self):
        """test that when fruit (apples) is bought before 7pm on a weekday, no discount applies"""
        dt = datetime.datetime(2026, 4, 15, 13, 20)
        disc_items = coles.discount_of_the_day('Apples', 2, 4, dt)
        self.assertEqual(disc_items, 0)

    def test_discount_of_day_wkday_before7pm_bananas_0(self):
        """test that when fruit (bananas) is bought before 7pm on a weekday, no discount applies"""
        dt = datetime.datetime(2026, 4, 14, 18, 59)
        disc_items = coles.discount_of_the_day('Bananas', 5, 5, dt)
        self.assertEqual(disc_items, 0)

    def test_discount_of_day_wkend_bananas_0(self):
        """test that when fruit (bananas) is bought on a weekend after 7pm, no discount applies"""
        dt = datetime.datetime(2026, 4, 18, 19, 59)
        disc_items = coles.discount_of_the_day('Bananas', 5, 5, dt)
        self.assertEqual(disc_items, 0)

    def test_discount_of_day_wkend_apples_0(self):
        """test that when fruit (apples) is bought on a weekend after 7pm, no discount applies"""
        dt = datetime.datetime(2026, 4, 19, 22, 30)
        disc_items = coles.discount_of_the_day('Apples', 6, 12, dt)
        self.assertEqual(disc_items, 0)


    # december and january juice, cake, and ice-cream - 50%
    def test_juice_discount_dec_50(self):
        """test that when a customer buys juices in December, 50% discount applies"""
        dt = datetime.datetime(2026, 12, 4, 16, 1)
        disc_items = coles.discount_of_the_day('Juice', 3, 12, dt)
        self.assertEqual(disc_items, 6)

    def test_juice_discount_jan_50(self):
        """test that when a customer buys juices in january, 50% discount applies"""
        dt = datetime.datetime(2027, 1, 29, 15, 13)
        disc_items = coles.discount_of_the_day('Juice', 5, 20, dt)
        self.assertEqual(disc_items, 10)

    def test_juice_discount_notdecjan_0(self):
        """test that when a customer buys juices outside of December/January window, no discount applies"""
        dt = datetime.datetime(2027, 2, 1, 14, 7)
        disc_items = coles.discount_of_the_day('Juice', 2, 8, dt)
        self.assertEqual(disc_items, 0)

    
    def test_cake_discount_dec_50(self):
        """test that when a customer buys cake in December, 50% discount applies"""
        dt = datetime.datetime(2026, 12, 13, 13, 13)
        disc_items = coles.discount_of_the_day('Cake', 1, 20, dt)
        self.assertEqual(disc_items, 10)

    def test_cake_discount_jan_50(self):
        """test that when a customer buys cake in January, 50% discount applies"""
        dt = datetime.datetime(2027, 1, 1, 13, 1)
        disc_items = coles.discount_of_the_day('Cake', 2, 40, dt)
        self.assertEqual(disc_items, 20)

    def test_cake_discount_notdecjan_0(self):
        """test that when a customer buys cake outside of December/January window, no discount applies"""
        dt = datetime.datetime(2026, 4, 18, 18, 18)
        disc_items = coles.discount_of_the_day('Cake', 3, 60, dt)
        self.assertEqual(disc_items, 0)


    def test_icecream_discount_dec_50(self):
        """test that when a customer buys ice-cream in December, 50% discount applies"""
        dt = datetime.datetime(2026, 12, 28, 13, 13)
        disc_items = coles.discount_of_the_day('Ice-cream', 3, 30, dt)
        self.assertEqual(disc_items, 15)

    def test_icecream_discount_jan_50(self):
        """test that when a customer buys ice-cream in January, 50% discount applies"""
        dt = datetime.datetime(2027, 1, 1, 22, 22)
        disc_items = coles.discount_of_the_day('Ice-cream', 5, 50, dt)
        self.assertEqual(disc_items, 25)

    def test_icecream_discount_notdecjan_0(self):
        """test that when a customer buys ice-cream outside of December/January window, no discount applies"""
        dt = datetime.datetime(2026, 4, 19, 18, 18)
        disc_items = coles.discount_of_the_day('Ice-cream', 1, 10, dt)
        self.assertEqual(disc_items, 0)


    # conflicting rules - priority test - juice weekend in december
    def test_juice_wkend_dec_conflicting_discounts(self):
        """test that when a customer purchases three juices on a weekend in december, weekend third juice free discount applies"""
        dt = datetime.datetime(2026, 12, 5, 7, 12)
        disc_items = coles.discount_of_the_day('Juice', 6, 24, dt)
        self.assertEqual(disc_items, 8)     # weekend juice discount higher priority than Dec 50% on juice

    

class TestAustraliaDayDiscount(unittest.TestCase):
    """
    class for testing Australia day discount function.

    The five discount scenarios have been designed in the theme of Australian produce (Eggs, Apples, Bananas (assuming produced/grown in Australia),Wines (vineyards), and Beers (breweries)),
    as well as, promoting healthy snacks and alternatives - focusing the largest discounts on zero-alcohol options and on water, apples, and bananas.
    
    Five discount scenarios:
        1. Before 11 am, when a customer buys 2 or more eggs they recieve 40% off. Supports farmers and incentivises breakfast/brunch at home.
        2. Before 3 pm, when a customer buys more than 3 wine items, they receive 60% off. Celebrating Australian vineyards.
        3. Before 3 pm, when a customer buys more than 2 beer items, they receive 50% off. Celebrating Australian breweries.
        4. Before 1 pm, when a customer buys more than 2 zero-alcohol items, they recieve 80% off. Promoting alcohol-free alternatives.
        5. Before 6 pm, when a customer buys water, apples, or bananas, they recieve 75% off. Promoting healthy choices and snacks.

    For each discount scenario, there are at least three test scenarios, which test a discounted circumstance, non-discounted circumstance because of quantity, and a non-discounted circumstance
    because of time. Within these scenarios, boundaries are also tested to ensure time and quantity restrictions have been implemented correctly.

    Test input has been created based off the discount scenario (e.g., product (eggs), quantity (2 or more), and time (before 11 am)), utilising the discounted, non-discounted, and boundaries
    to design the input.
    """

    
    # discount 1: 40% off of eggs when 2 or more egg items are purchased before 11 am
    def test_2ormore_eggs_ausday_40(self):
        """
        Test scenario:
            test that when a customer buys 2 or more eggs before 11 am, they receive 40% off the price of their eggs.
        
        Testing technique:
            Boundary value analysis - quantity of 2 and purchase at 10:59 am.

        Test input creation:
            A datetime object for the 26th of January at 10:59 am is used to satisfy the time condition.
            A quantity of 2 eggs is created to satisfy the product quantity and product name condition.
        """
        dt = datetime.datetime(2026, 1, 26, 10, 59)
        aus_disc_items = coles.discount_Australia_day('Eggs', 2, 10, dt)
        self.assertEqual(aus_disc_items, 4)

    
    def test_lessthan2_eggs_ausday_0(self):
        """
        Test scenario:
            test that when a customer buys less than 2 eggs before 11 am, they receive no discount.

        Testing technique:
            Negative testing - discount does not apply when only 1 egg item is purchased.

        Test input creation:
            A datetime object for the 26th of January at 9:52 am is used to satisfy the time condition.
            A quantity of 1 eggs is created to satisfy the product name condition but not the product quantity condition.
        """
        dt = datetime.datetime(2026, 1, 26, 9, 52)
        aus_disc_items = coles.discount_Australia_day('Eggs', 1, 5, dt)
        self.assertEqual(aus_disc_items, 0)

    
    
    def test_2ormore_eggs_ausday_0(self):
        """
        Test scenario:
            test that when a customer buys 2 or more eggs at 11 am, they receive no discount

        Testing technique:
            Negative testing - discount does not apply at 11 am or afterwards.
            Boundary testing - testing before 11 am boundary.

        Test input creation:
            A datetime object for the 26th of January at 11:00 am is used to not meet the time condition.
            A quantity of 4 eggs is created to satisfy the product quantity and product name condition.
        """
        dt = datetime.datetime(2026, 1, 26, 11, 0)
        aus_disc_items = coles.discount_Australia_day('Eggs', 4, 20, dt)
        self.assertEqual(aus_disc_items, 0)


    
    
    # discount 2: 60% off of wine when more than 3 items are purchased before 3 pm
    def test_morethan3_wine_ausday_60(self):
        """
        Test scenario:
            test that when a customer buys more than 3 wine items before 3 pm, they receive 60% off.

        Testing technique:
            Positive testing - discount does apply when more than 3 Wines are bought before 3 pm.
            Boundary testing - a quantity of 4 chosen as this is the minimum required to satisfy the condition, as well as 2:59 pm being the last minute satisfying time requirement.

        Test input creation:
            A datetime object for the 26th of January at 14:59 am is used to satisfy the time condition.
            A quantity of 4 Wine is created to satisfy the product quantity and product name condition.
        """
        dt = datetime.datetime(2026, 1, 26, 14, 59)
        aus_disc_items = coles.discount_Australia_day('Wine', 4, 200, dt)
        self.assertEqual(aus_disc_items, 120)

    
    
    def test_3_wine_ausday_0(self):
        """
        Test scenario:
            test that when a customer buys 3 or less wine items before 3 pm, they receive no discount

        Testing technique:
            Negative testing - 3 wine items does not meet the > 3 quantity requirement.
            boundary teststing - quantity boundary test at 3 items.

        Test input creation:
            A datetime object for the 26th of January at 14:22 pm is used to meet the time condition.
            A quantity of 3 wine is created to satisfy the product quantity and product name condition.   
        """
        dt = datetime.datetime(2026, 1, 26, 14, 22)
        aus_disc_items = coles.discount_Australia_day('Wine', 3, 150, dt)
        self.assertEqual(aus_disc_items, 0)

    
    
    def test_morethan3_wine_ausday_0(self):
        """
        Test scenario:
            test that when a customer buys more than 3 wine items at 3 pm, they receive no discount.
        
        Testing technique:
            Negative testing - purchase is made at 3pm, not before 3 pm.
            Boundary testing - testing 3pm boundary, with all other discount conditions met (product name, quantity, date)

        Test input creation:
            A datetime object for the 26th of January at 15:00 pm is used to not meet the time condition.
            A quantity of 5 wine is created to satisfy the product quantity and product name condition.
        """
        dt = datetime.datetime(2026, 1, 26, 15, 0)
        aus_disc_items = coles.discount_Australia_day('Wine', 5, 250, dt)
        self.assertEqual(aus_disc_items, 0)


    
    
    # discount 3: 50% off beer when more than 2 items are purchased before 3 pm
    def test_morethan2_beer_ausday_50(self):
        """
        Test scenario:
            test that when a customer buys more than 2 beer items before 3 pm, they receive 50% off.

        Testing technique:
            Positive testing - purchase is made before 3pm and meets product minimum of 3 (>2).
            Boundary testing - purchase quantity meets minimum requirement of 3. Purchase made at 2:59 pm on discount time boundary.

        Test input creation:
            A datetime object for the 26th of January at 14:59 pm is used to meet the time condition.
            A quantity of 3 Beer is created to satisfy the product quantity and product name condition.
        """
        dt = datetime.datetime(2026, 1, 26, 14, 59)
        aus_disc_items = coles.discount_Australia_day('Beer', 3, 75, dt)
        self.assertEqual(aus_disc_items, 37.5)

    
    def test_2_beer_ausday_0(self):
        """
        Test scenario:
            test that when a customer buys 2 or less beer items before 3 pm, they receive no discount.

        Testing technique:
            Negative testing - product quantity does not satisfy > 2 condition.
            Boundary testing - product boundary of 2 tested.

        Test input creation:
            A datetime object for the 26th of January at 13:11 pm is used to not meet the time condition.
            A quantity of 2 beer is created to satisfy product name condition but not the product quantity.    
        """
        dt = datetime.datetime(2026, 1, 26, 13, 11)
        aus_disc_items = coles.discount_Australia_day('Beer', 2, 50, dt)
        self.assertEqual(aus_disc_items, 0)

    
    def test_morethan2_beer_ausday_0(self):
        """
        Test scenario:
            test that when a customer buys more than 2 beer items at 3 pm, they receive no discount.

        Testing technique:
            Negative testing - time does not satisfy before 3pm requirement.
            Boundary testing - time boundary of 3pm tested to test negative case.

        Test input creation:
            A datetime object for the 26th of January at 15:00 pm is used to not meet the time condition.
            A quantity of 4 beer is created to satisfy the product quantity and product name condition.

        """
        dt = datetime.datetime(2026, 1, 26, 15, 0)
        aus_disc_items = coles.discount_Australia_day('Beer', 4, 250, dt)
        self.assertEqual(aus_disc_items, 0)


    
    
    # discount 4: 80% off zero-alcohol items when more than 2 items are bought before 1 pm
    def test_morethan2_zero_alc_ausday_80(self):
        """
        Test scenario:
            test that when a customer buys more than 2 zero-alcohol items before 1 pm, they receive 80% off.
        
        Testing technique:
            Positive testing - product name, quantity, and time conditions are met.
            Boundary testing - 12:59 pm purchase to test boundary of before 1pm and 3 items purchased to test quantity boundary.

        Test input creation:
            A datetime object for the 26th of January at 12:59 pm is used to meet the time condition.
            A quantity of 3 zero alcohol items is created to satisfy the product quantity and product name condition.
        """
        dt = datetime.datetime(2026, 1, 26, 12, 59)
        aus_disc_items = coles.discount_Australia_day('Zero Alcohol', 3, 60, dt)
        self.assertEqual(aus_disc_items, 48)

    
    
    def test_2_zero_alc_ausday_0(self):
        """
        Test scenario:
            test that when a customer buys 2 or less zero alcohol items before 1 pm, they receive no discount.
        
        Testing technique:
            Negative testing - testing discount does not apply when 2 zero alcohol items are purchased.
            Boundary testing - testing > 2 product quantity boundary.

        Test input creation:
            A datetime object for the 26th of January at 10:10 am is used to meet the time condition.
            A quantity of 2 zero alcohol items is created to satisfy the product name condition but not the product quantity.
        """
        dt = datetime.datetime(2026, 1, 26, 10, 10)
        aus_disc_items = coles.discount_Australia_day('Zero Alcohol', 2, 40, dt)
        self.assertEqual(aus_disc_items, 0)

    
    
    def test_morethan2_zero_alc_ausday_0(self):
        """
        Test scenario:
            test that when a customer buys more than 2 zero alcohol items at 1 pm, they receive no discount.
        
        Testing technique:
            Negative testing - purchase made at 1pm, not before 1pm.
            Boundary testing - testing no discount applies at 1 pm, only before.

        Test input creation:
            A datetime object for the 26th of January at 13:00 pm is used to not meet the time condition.
            A quantity of 4 zero alcohol items is created to satisfy the product quantity and product name condition.
        """
        dt = datetime.datetime(2026, 1, 26, 13, 0)
        aus_disc_items = coles.discount_Australia_day('Zero Alcohol', 4, 80, dt)
        self.assertEqual(aus_disc_items, 0)

    
    
    
    # discount 5: 75% off water, apples, and bananas before 6 pm
    def test_healthy_snack_water_ausday_before6pm_75(self):
        """
        Test scenario:
            test that when a customer buys water before 6 pm, they receive 75% off.

        Testing technique:
            Positive testing - purchase made before 6pm, and product name meets requirement.
            Boundary testing - testing before 6pm boundary, with pruchase made at 5:59 pm.

        Test input creation:
            A datetime object for the 26th of January at 17:59 pm is used to meet the time condition.
            A quantity of 3 water items is created to satisfy the product quantity and product name condition.
        
        """
        dt = datetime.datetime(2026, 1, 26, 17, 59)
        aus_disc_items = coles.discount_Australia_day('Water', 3, 15, dt)
        self.assertEqual(aus_disc_items, 11.25)

    
    
    def test_healthy_snack_apples_ausday_before6pm_75(self):
        """
        Test scenario:
            test that when a customer buys apples before 6 pm, they receive 75% off.
        
        Testing technique:
            Positive testing - product name and purchase time meet requirements.

        Test input creation:
            A datetime object for the 26th of January at 13:13 pm is used to meet the time condition.
            A quantity of 3 apples is created to satisfy the product name condition.
        """
        dt = datetime.datetime(2026, 1, 26, 13, 13)
        aus_disc_items = coles.discount_Australia_day('Apples', 3, 6, dt)
        self.assertEqual(aus_disc_items, 4.5)

    
    
    def test_healthy_snack_bananas_ausday_before6pm_75(self):
        """
        Testing scenario:
            test that when a customer buys bananas before 6 pm, they receive 75% off.

        Testing technique:
            Positive testing - product name and purchase time meet requirements.
        
        Test input creation:
            A datetime object for the 26th of January at 11:36 am is used to meet the time condition.
            A quantity of 6 bananas is created to satisfy the product name condition.
        """
        dt = datetime.datetime(2026, 1, 26, 11, 36)
        aus_disc_items = coles.discount_Australia_day('Bananas', 6, 6, dt)
        self.assertEqual(aus_disc_items, 4.5)


    def test_healthy_snack_bananas_ausday_6pm_0(self):
        """
        Test scenario:
            test that when a customer buys bananas at or after 6 pm, they receive no discount.
        
        Testing technique:
            Negative testing - purchase time does not meet time period condition.
            Boundary testing - test of before 6 pm boundary.

        Test input creation:
            A datetime object for the 26th of January at 18:00 pm is used to meet the time condition.
            A quantity of 8 bananas is created to satisfy the product name condition.
        """
        dt = datetime.datetime(2026, 1, 26, 18, 00)
        aus_disc_items = coles.discount_Australia_day('Bananas', 8, 8, dt)
        self.assertEqual(aus_disc_items, 0)

    
    def test_healthy_snack_apples_ausday_after6pm_0(self):
        """
        Test scenario:
            test that when a customer buys apples at or after 6 pm, they receive no discount.
        
        Testing technique:
            Negative testing - time conditions not met, purchase after 6pm.

        Test input creation:
            A datetime object for the 26th of January at 20:20 pm is used to not meet the time condition.
            A quantity of 4 apples is created to satisfy the product name condition.
        """
        dt = datetime.datetime(2026, 1, 26, 20, 20)
        aus_disc_items = coles.discount_Australia_day('Apples', 4, 8, dt)
        self.assertEqual(aus_disc_items, 0)

    
    
    def test_healthy_snack_water_ausday_after6pm_0(self):
        """
        Test scenario:
            test that when a customer buys water at or after6 pm, they receive no discount.
        
        Testing technique:
            Negative testing - time condition not met, purchase after 6pm.

        Test input creation:
            A datetime object for the 26th of January at 19:17 pm is used to not meet the time condition.
            A quantity of 2 water items is created to satisfy the product name condition.
        """
        dt = datetime.datetime(2026, 1, 26, 19, 17)
        aus_disc_items = coles.discount_Australia_day('Water', 2, 10, dt)
        self.assertEqual(aus_disc_items, 0)


   

    
unittest.main()