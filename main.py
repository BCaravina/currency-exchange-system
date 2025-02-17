import tkinter as tk
from tkinter import ttk 
from tkcalendar import DateEntry
import requests

api_request = requests.get("https://economia.awesomeapi.com.br/json/all")
currencies_dictionary = api_request.json()
currencies_list = list(currencies_dictionary.keys())

def get_single_rate():
    '''
    Makes API call and returns single date exchange rate of user selected currency and date to Brazilian Real.
    '''
    currency = combobox_single_date.get()
    date = str(date_entry_single.get_date())
    date_api_format = date.replace('-', '')
    api_request = requests.get(f'https://economia.awesomeapi.com.br/json/daily/{currency}/?start_date={date_api_format}&end_date={date_api_format}')
    exchange_rate = api_request.json()
    try:
        currency_value = float(exchange_rate[0]['bid'])
        label_single_currency_output['text'] = f"Exchange rate for {currency} in {date} was R${currency_value:,.3f}"
    except IndexError: 
        label_single_currency_output['text'] = 'Unexpected error. Please try again.'


def select_file():
    ...


def get_multiple_rates():
    ...


window = tk.Tk()
window.title("Currency Exchange Rate System")

title_single_currency = tk.Label(text="Single Currency Exchange Rate", borderwidth=2, relief="solid")
title_single_currency.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

label_single_currency = tk.Label(text="Choose desired currency:", anchor='e')
label_single_currency.grid(row=1, column=0, columnspan=2, sticky="nswe", padx=10, pady=10)

combobox_single_date = ttk.Combobox(values=currencies_list)
combobox_single_date.grid(row=1, column=2, sticky="nswe", padx=10, pady=10)

label_single_currency = tk.Label(text="Select exchange rate date:", anchor='e')
label_single_currency.grid(row=2, column=0, columnspan=2, sticky="nswe", padx=10, pady=10)

# date_entry_single = DateEntry(locale='pt-br') # this would be the option for brazilian format of date and text in portuguese
date_entry_single = DateEntry()
date_entry_single.grid(row=2, column=2, sticky='nswe', padx=10, pady=10)

button_single_currency = tk.Button(text="Get Rate", command=get_single_rate)
button_single_currency.grid(row=3, column=2, padx=10, pady=10, sticky="nswe")

label_single_currency_output = tk.Label(text="", anchor='w')
label_single_currency_output.grid(row=3, column=0, columnspan=2, sticky="nswe", padx=10, pady=10)

title_multiple_currencies = tk.Label(text="Multiple Currencies Exchange Rates", borderwidth=2, relief="solid")
title_multiple_currencies.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

label_select_file = tk.Label(text="Please, select an Excel file that has 'Currency' written on cell A1.", anchor='w')
label_select_file.grid(row=5, column=0, columnspan=2, sticky="nswe", padx=10, pady=10)

button_select_file = tk.Button(text="Select File", command=select_file)
button_select_file.grid(row=5, column=2, padx=10, pady=10, sticky="nswe")

label_file_description = tk.Label(text="No file currently selected.", borderwidth=2, relief="solid")
label_file_description.grid(row=6, column=2, sticky="nswe", padx=10, pady=10)

label_initial_date = tk.Label(text="Choose start date:", anchor='e')
label_initial_date.grid(row=7, column=0, sticky='nswe', padx=10, pady=10)
date_entry_initial = DateEntry()
date_entry_initial.grid(row=7, column=1, sticky='nswe', padx=10, pady=10)

label_final_date = tk.Label(text="Choose end date:", anchor='e')
label_final_date.grid(row=8, column=0, sticky='nswe', padx=10, pady=10)
date_entry_final =  DateEntry()
date_entry_final.grid(row=8, column=1, sticky='nswe', padx=10, pady=10)

label_update_success = tk.Label(text="")
label_update_success.grid(row=9, column=0, columnspan=3, sticky='nswe', padx=10, pady=10)

button_update_currencies = tk.Button(text="Get Rates", command=get_multiple_rates)
button_update_currencies.grid(row=7, column=2, sticky='nswe', padx=10, pady=10)

button_exit = tk.Button(text="Exit System", command=window.quit)
button_exit.grid(row=10, column=2, sticky='nswe', padx=10, pady=10)

window.mainloop()