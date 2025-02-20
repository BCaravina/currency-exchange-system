import tkinter as tk
from time import strftime
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkcalendar import DateEntry
from datetime import datetime
import pandas as pd
import requests

api_request = requests.get("https://economia.awesomeapi.com.br/json/all")
currencies_dictionary = api_request.json()
currencies_list = list(currencies_dictionary.keys())

def get_single_rate():
    """
    Makes API call and returns single date exchange rate of user selected currency and date to Brazilian Real.
    """
    currency = combobox_single_date.get()
    single_date = str(date_entry_single.get_date())
    date_api_format = single_date.replace('-', '')
    request = requests.get(f'https://economia.awesomeapi.com.br/json/daily/{currency}/1?start_date={date_api_format}&end_date={date_api_format}', timeout=10)
    exchange_rate = request.json()
    try:
        currency_value = float(exchange_rate[0]['bid'])
        label_single_currency_output['text'] = f"Exchange rate for {currency} in {single_date} was R${currency_value:,.3f}"
    except IndexError:
        label_single_currency_output['text'] = 'Unexpected error. Please try again.'


def select_file():
    """
    Prompts user to select an Excel file and returns message with the path of the selected file.
    """
    file_path = askopenfilename(title="Select Excel File", filetypes=[("Excel file","*.xlsx"),("Excel file 97-2003","*.xls")])
    file_path_var.set(file_path)

    if file_path:
        label_selected_file['text'] = f"File selected: {file_path}"


def get_multiple_rates():
    """
    After user has selected a valid Excel file with the desired currencies and date period, API call is made to retrieve the exchange rates.
    Returns a new Excel file with the dates and corresponding exchange rates for each coin.
    """
    df = pd.read_excel(file_path_var.get())
    currencies = df.iloc[:, 0]

    start_date = str(date_entry_initial.get_date()).replace("-", "")
    end_date = str(date_entry_final.get_date()).replace("-", "")
    number_of_days = (datetime.strptime(end_date, "%Y%m%d") - datetime.strptime(start_date, "%Y%m%d")).days

    export_df = pd.DataFrame()
    for currency in currencies:
        try:
            link = f'https://economia.awesomeapi.com.br/json/daily/{currency}/{number_of_days}?start_date={start_date}&end_date={end_date}'
            request = requests.get(link, timeout=10)
            exchange_rates = request.json()

            for rate in exchange_rates:
                bid = float(rate['bid'])
                timestamp = datetime.fromtimestamp(int(rate['timestamp']))
                date_from_timestamp = timestamp.strftime('%m/%d/%Y')

                # COLUMN A -> DATES
                # COLUM B -> CURRENCY #1
                # COLUM C -> CURRENCY #2
                # COLUM D -> CURRENCY #3 ETC, ETC
                # COLUMN A + ROW 1 = BID 1 FOR CURRENCY #1

                export_df[date_from_timestamp] = date_from_timestamp
                export_df.loc[currency] = bid

                # print(f'Currency: {currency} - Bid: R$ {bid:,} - Date: {date_from_timestamp}')
        except Exception as e:
            print(f"ERROR: {e}")

        print(export_df)
        export_df.to_excel("Currency_Rates.xlsx", index=False)

window = tk.Tk()
window.title("Currency Exchange Rate System")

title_single_currency = tk.Label(text="Single Currency Exchange Rate", borderwidth=2, relief="solid")
title_single_currency.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

label_single_currency = tk.Label(text="Select currency:", anchor='e')
label_single_currency.grid(row=1, column=0, columnspan=2, sticky="nswe", padx=10, pady=10)

combobox_single_date = ttk.Combobox(values=currencies_list)
combobox_single_date.grid(row=1, column=2, sticky="nswe", padx=10, pady=10)

label_single_currency = tk.Label(text="Select date:", anchor='e')
label_single_currency.grid(row=2, column=0, columnspan=2, sticky="nswe", padx=10, pady=10)

date_entry_single = DateEntry()
date_entry_single.grid(row=2, column=2, sticky='nswe', padx=10, pady=10)

button_single_currency = tk.Button(text="Get Rate", command=get_single_rate)
button_single_currency.grid(row=3, column=2, padx=10, pady=10, sticky="nswe")

label_single_currency_output = tk.Label(text="", anchor='e')
label_single_currency_output.grid(row=3, column=0, columnspan=2, sticky="nswe", padx=10, pady=10)

title_multiple_currencies = tk.Label(text="Multiple Currencies Exchange Rates", borderwidth=2, relief="solid")
title_multiple_currencies.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

label_file_instruction = tk.Label(text="Please, select an Excel file that contains list of currencies on Column A1", anchor='e')
label_file_instruction.grid(row=5, column=0, columnspan=2, sticky="nswe", padx=10, pady=10)

button_select_file = tk.Button(text="Select File", command=select_file)
button_select_file.grid(row=5, column=2, padx=10, pady=10, sticky="nswe")

file_path_var = tk.StringVar()
label_selected_file = tk.Label(text="No file currently selected.", anchor='e')
label_selected_file.grid(row=6, column=0, columnspan=3, sticky="nswe", padx=10, pady=10)

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
