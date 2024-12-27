import pathlib
import textwrap
import time
from dotenv import load_dotenv
import  os
import google.generativeai as genai
import google.ai.generativelanguage as glm

from IPython import display
from IPython.display import Markdown


# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')

# Configure Gemini API
genai.configure(api_key=api_key)

# 01 create custom funs

def get_order_status(order_id: str) -> str:
    """Fetches the status of a given order ID."""
    # Mock data for example purposes
    order_statuses = {
        "12345": "Shipped",
        "67890": "Processing",
        "11223": "Delivered"
    }
    return order_statuses.get(order_id, "Order ID not found.")

def initiate_return(order_id: str, reason: str) -> str:
    """Initiates a return for a given order ID with a specified reason."""
    # Mock data for example purposes
    if order_id in ["12345", "67890", "11223"]:
        return f"Return initiated for order {order_id} due to: {reason}."
    else:
        return "Order ID not found. Cannot initiate return."

def cancel_order(order_id: str) -> str:
    """Cancels a given order ID if possible."""
    # Mock data for example purposes
    order_statuses = {
        "12345": "Shipped",
        "67890": "Processing",
        "11223": "Delivered"
    }
    if order_id in order_statuses:
        if order_statuses[order_id] == "Processing":
            return f"Order {order_id} has been canceled successfully."
        else:
            return f"Order {order_id} cannot be canceled as it is already {order_statuses[order_id]}."
    else:
        return "Order ID not found. Cannot cancel order."

def update_shipping_address(order_id: str, new_address: str) -> str:
    """Updates the shipping address for a given order ID."""
    # Mock data for example purposes
    if order_id in ["12345", "67890", "11223"]:
        return f"Shipping address for order {order_id} has been updated to: {new_address}."
    else:
        return "Order ID not found. Cannot update shipping address."

def track_shipment(tracking_number: str) -> str:
    """Tracks the shipment with the given tracking number."""
    # Mock data for example purposes
    tracking_info = {
        "TRACK123": "In Transit",
        "TRACK456": "Delivered",
        "TRACK789": "Out for Delivery"
    }
    return tracking_info.get(tracking_number, "Tracking number not found.")

def apply_discount(order_id: str, discount_code: str) -> str:
    """Applies a discount to the given order ID."""
    # Mock data for example purposes
    valid_discount_codes = ["DISCOUNT10", "SAVE20"]
    if order_id in ["12345", "67890", "11223"]:
        if discount_code in valid_discount_codes:
            return f"Discount code {discount_code} applied to order {order_id}."
        else:
            return f"Invalid discount code: {discount_code}."
    else:
        return "Order ID not found. Cannot apply discount."

def change_payment_method(order_id: str, payment_method: str) -> str:
    """Changes the payment method for a given order ID."""
    # Mock data for example purposes
    if order_id in ["12345", "67890", "11223"]:
        return f"Payment method for order {order_id} has been changed to: {payment_method}."
    else:
        return "Order ID not found. Cannot change payment method."

def provide_invoice(order_id: str) -> str:
    """Provides an invoice for the given order ID."""
    # Mock data for example purposes
    if order_id in ["12345", "67890", "11223"]:
        return f"Invoice for order {order_id} has been sent to your email."
    else:
        return "Order ID not found. Cannot provide invoice."

def extend_warranty(order_id: str, years: int) -> str:
    """Extends the warranty for a given order ID."""
    # Mock data for example purposes
    if order_id in ["12345", "67890", "11223"]:
        return f"Warranty for order {order_id} has been extended by {years} years."
    else:
        return "Order ID not found. Cannot extend warranty."

def check_product_availability(product_id: str) -> str:
    """Checks the availability of a product with the given product ID."""
    # Mock data for example purposes
    product_availability = {
        "PROD123": "In Stock",
        "PROD456": "Out of Stock",
        "PROD789": "Limited Stock"
    }
    return product_availability.get(product_id, "Product ID not found.")

# initialize the model
model = genai.GenerativeModel(
    model_name='gemini-pro',
    tools=[get_order_status, initiate_return] # list of all available tools
)
#model._tools.to_proto()

# 03 model in chat mode for function calling
chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message('What is the status of order 12345?')
print(response.text)

response = chat.send_message('I want to return order 11223 because it is defective.')
print(response.text)

for content in chat.history:
    part = content.parts[0]
    print(content.role, "->", type(part).to_dict(part))
    print('-'*80)