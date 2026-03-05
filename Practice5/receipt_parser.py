import re
import json

# read receipt file
with open("raw.txt", "r", encoding="utf-8") as file:
    data = file.read()

# extract product names (line after number.)
products = re.findall(r"\d+\.\n(.+)", data)

# extract prices (numbers like 308,00)
prices = re.findall(r"\n(\d[\d\s]*,\d{2})\nСтоимость", data)

# clean prices (remove spaces and convert to float)
prices = [float(p.replace(" ", "").replace(",", ".")) for p in prices]

# extract total
total_match = re.search(r"ИТОГО:\n([\d\s]+,\d{2})", data)
total = total_match.group(1) if total_match else None

# extract date and time
datetime_match = re.search(r"Время:\s(\d{2}\.\d{2}\.\d{4})\s(\d{2}:\d{2}:\d{2})", data)

date = datetime_match.group(1) if datetime_match else None
time = datetime_match.group(2) if datetime_match else None

# payment method
payment = "Банковская карта" if "Банковская карта" in data else "Unknown"

# structured result
receipt = {
    "products": products,
    "prices": prices,
    "total": total,
    "date": date,
    "time": time,
    "payment_method": payment
}

print(json.dumps(receipt, indent=4, ensure_ascii=False))