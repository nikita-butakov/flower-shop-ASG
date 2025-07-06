import requests
import random
import time
import string

URL = "https://shoppng.online/order"

flowers = ["romantic_roses", "spring_tulips", "blossom_mix"]

def random_name():
    first_names = ["Anna", "John", "Emma", "Michael", "Olivia", "David", "Sophia", "Daniel"]
    last_names = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Miller", "Davis"]
    return random.choice(first_names) + " " + random.choice(last_names)

def random_address():
    streets = ["Main St", "Oak St", "Pine Ave", "Maple Rd", "Cedar Blvd", "Elm St"]
    number = random.randint(1, 9999)
    return f"{number} {random.choice(streets)}"

def make_order():
    data = {
        "name": random_name(),
        "address": random_address(),
        "flower": random.choice(flowers)
    }
    try:
        response = requests.post(URL, json=data, timeout=5)
        if response.status_code == 200:
            print(f"Order successful: {data}")
        else:
            print(f"Order failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Request error: {e}")

if __name__ == "__main__":
    orders_to_send = 3000  # total number of orders to simulate
    delay = 8  # delay between each request in seconds

    for _ in range(orders_to_send):
        make_order()
        time.sleep(delay)

