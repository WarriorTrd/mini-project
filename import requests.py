import pandas as pd
import sqlite3

df = pd.read_csv(r"D:\warrior\Desktop\mini project\EUR.csv") 

df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')


conn = sqlite3.connect('exchange_rates.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS exchange_rates (
        date TEXT PRIMARY KEY,
        price REAL
    )
''')


for index, row in df.iterrows():
    cursor.execute('''
        INSERT OR REPLACE INTO exchange_rates (date, price) VALUES (?, ?)
    ''', (row['Date'].strftime('%d-%m-%Y'), row['Price']))

conn.commit()


def rate_for_specific_day(date):
    cursor.execute('''
        SELECT price FROM exchange_rates WHERE date = ?
    ''', (date,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


def convert_currency(amount, from_currency, to_currency, date):
    rate_from = rate_for_specific_day(date)
    if rate_from is None:
        return f"No rate available for {from_currency} to {to_currency} on {date}."
    
   
    if from_currency == 'EUR' and to_currency == 'USD': 
        converted_amount = amount * rate_from
    elif from_currency == 'USD' and to_currency == 'EUR':  
        converted_amount = amount / rate_from
    else:
        return f"Conversion from {from_currency} to {to_currency} is not supported."
    
    return converted_amount


def show_rate_for_date(date):
    rate = rate_for_specific_day(date)
    if rate is not None:
        print(f"Exchange rate for {date} is: {rate} EUR")
    else:
        print(f"No data available for {date}.")


def main():
    while True:
        print("\nWelcome to the Currency Converter!")
        print("1. Show exchange rate for a specific date")
        print("2. Convert currency")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            date = input("Enter the date (DD-MM-YYYY): ")
            show_rate_for_date(date)

        elif choice == '2':
            amount = float(input("Enter the amount to convert: "))
            from_currency = input("Enter the base currency (EUR, USD): ").upper()
            to_currency = input("Enter the target currency (EUR, USD): ").upper()
            date = input("Enter the date for conversion (DD-MM-YYYY): ")

            converted_amount = convert_currency(amount, from_currency, to_currency, date)
            print(f"Converted amount: {converted_amount}")

        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

conn.close()
