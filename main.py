import tkinter as tk
import requests as req
import asyncio
from datetime import datetime

PRICES_ENDPOINT = "https://www.sahkohinta-api.fi/api/v1/halpa?tunnit=24&tulos=sarja&aikaraja="
now = datetime.now().date()

def get_color_by_price(price):
    normalized_price = min(price / 6, 1.0)

    red = int(255 * normalized_price)
    green = int(255 * (1 - normalized_price))

    return f'#{red:02x}{green:02x}00'

def update_price_labels(labels_list):
    response = req.get(PRICES_ENDPOINT + str(now))

    if (response == 429):
        return

    response_json = response.json()

    print(f'{response_json}')

    for i, entry in enumerate(response_json):
        if i < len(labels_list):
            price = float(entry['hinta'])
            price_text = str(price)
            labels_list[i].configure(text=price_text, bg = get_color_by_price(price))

def main():
    root = tk.Tk()
    root.title("Sähkön hinta")
    root.resizable(False, False)

    main_canvas = tk.Canvas()
    main_canvas.pack(padx = 15, pady = 15)

    header_label = tk.Label(main_canvas, text= f'Sähkön hinta {now.day}.{now.month}.{now.year}', font = ('Arial', 16, 'bold'))
    header_label.grid(row = 0, columnspan = 24, padx = 10, pady = 10, sticky = 'NSEW')

    time_labels = [tk.Label(main_canvas, font = ('Arial', 12)) for _ in range(24)]
    hour_labels = [tk.Label(main_canvas, font = ('Arial', 12)) for _ in range(24)]

    for i, label in enumerate(time_labels):
        label.configure(text = str(i + 1))
        label.grid(row = 1, column = i, sticky = 'NSEW')

    for i, label in enumerate(hour_labels):
        label.grid(row = 2, column = i, sticky = 'NSEW')

    update_price_labels(hour_labels)

    root.mainloop()

if __name__ == "__main__":
    main()
