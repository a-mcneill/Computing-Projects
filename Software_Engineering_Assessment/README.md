# Coles Checkout System - Software Engineering Assessment

A complete Python-based checkout system simulating the Coles online shopping workflow. This project demonstrates modular software design, a Test‑Driven Development (TDD) workflow, business‑logic implementation, data handling using pandas, and a comprehensive unittest suite validating all functional behaviour.

---

## Project Structure

Software_Engineering_Assessment/
│
├── coles.py               # Core business logic (eligibility, limits, discounts)
├── test_coles.py          # Full unittest suite covering all functions
├── main.py                # CLI application supplied as part of the university assessment
└── README.md              # Project documentation


---

## Overview

The system models a realistic retail checkout process, including:

- Customer age validation  
- Product eligibility (age restrictions, alcohol trading windows)  
- Quantity limits based on product, date, and time  
- Seasonal and event‑based discount rules  
- Delivery charge calculation  
- A complete CLI checkout workflow  
- A formatted receipt using pandas and tabulate

---

## Features

### 1. Input Validation
- Validates customer age (1–120)  
- Ensures product names exist and quantities are positive integers  

### 2. Product Eligibility
Implements rules for:
- Alcohol (age ≥ 18 + trading windows)  
- Cutting knives (age ≥ 15)  
- Cosmetic fillers (age ≥ 15)  
- Weekend vs weekday alcohol sale windows  

### 3. Quantity Limits
Dynamic restrictions based on:
- Product type  
- Month (e.g., ice‑cream Dec–Mar, eggs Jun–Jul)  
- Time of day (fruit before/after 7pm)  
- Holidays (Christmas Day, New Year’s Day)  

### 4. Discount Engine
Multiple discount types:
- Weekend juice “buy 2 get 1 free”  
- Fruit 50% off after 7pm on weekdays  
- December/January 50% off juice, cake, ice‑cream  
- Australia Day multi‑rule discount system  

### 5. Delivery Charges
Distance‑based pricing with:
- Tiered delivery fees  
- Weekday 10% discount for orders ≥ $50  
- Weekend 20% discount for orders ≥ $50  

### 6. Full CLI Application
`main.py` provides:
- User prompts  
- Product scanning  
- Cart building via pandas  
- Discount application  
- Delivery charge calculation  
- Receipt printing using tabulate

---

## Installation

### Requirements

Install dependencies:

```bash
pip install pandas tabulate
```

---

## Running the Application

```bash
python main.py
```

---

## Running Tests

```bash
python -m unittest test_coles.py
```

---

## Technologies Used

- Python 3.x  
- pandas  
- tabulate  
- unittest  




