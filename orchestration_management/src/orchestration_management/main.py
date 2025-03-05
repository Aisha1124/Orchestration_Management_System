from crewai.flow.flow import Flow, listen, start
from orchestration_management.crews.shop_crew.Shop_crew import MangerCrew
import os
import csv
import uuid

class ShopFlow(Flow):
    def __init__(self):
        super().__init__()
        self.shop_crew = MangerCrew()
        self.selected_product = None

    @start()
    def interaction_with_user(self):
        print("Welcome to our Agentic AI Shopping Mart!")
        user_input = input("What would you like to shop for today? ")
        
        # Get the selected product from the crew
        crew_output = self.shop_crew.crew().kickoff(inputs={"user_query": user_input})
        
        # Extract the output string from CrewOutput
        self.selected_product = str(crew_output)
        
        # Proceed to checkout
        return self.proceed_to_checkout()

    def proceed_to_checkout(self):
        # Parse the product details
        product_details = self.parse_product_details(self.selected_product)
        
        # Display product details
        print("\n--- Selected Product ---")
        print(f"Product ID: {product_details['pd_id']}")
        print(f"Product Name: {product_details['product_name']}")
        print(f"Quality: {product_details['quality']}")
        print(f"Price: ${product_details['price']}")
        
        # Collect checkout information
        checkout_info = self.collect_checkout_details()
        
        # Finalize and save order
        self.save_order(product_details, checkout_info)
        
        return self.selected_product

    def parse_product_details(self, product_string):
        # Clean and parse the product string
        # Remove any potential formatting artifacts
        product_string = product_string.replace('```text', '').replace('```', '').strip()
        
        # Split the product details
        details = {}
        for line in product_string.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                details[key] = value
        
        # Ensure all required keys are present
        required_keys = ['product_id', 'product_name', 'quality', 'price']
        for key in required_keys:
            if key not in details:
                details[key] = 'Unknown'
        
        # Rename keys to match previous implementation
        return {
            'pd_id': details.get('product_id', 'Unknown'),
            'product_name': details.get('product_name', 'Unknown'),
            'quality': details.get('quality', 'Unknown'),
            'price': details.get('price', '0').replace('$', '')
        }

    def collect_checkout_details(self):
        print("\n--- Checkout Details ---")
        checkout_info = {
            'customer_name': input("Enter your full name: "),
            'email': input("Enter your email address: "),
            'phone': input("Enter your phone number: "),
            'address': input("Enter your shipping address: ")
        }
        return checkout_info

    def save_order(self, product_details, checkout_info):
        # Create checkout directory if it doesn't exist
        os.makedirs('checkout', exist_ok=True)
        
        # Generate unique order ID
        order_id = str(uuid.uuid4())
        
        # Prepare file paths
        txt_filepath = os.path.join('checkout', f'order_{order_id}.txt')
        csv_filepath = os.path.join('checkout', f'order_{order_id}.csv')
        
        # Save TXT file
        with open(txt_filepath, 'w') as txt_file:
            txt_file.write("Order Details:\n")
            txt_file.write(f"Product ID: {product_details['pd_id']}\n")
            txt_file.write(f"Product Name: {product_details['product_name']}\n")
            txt_file.write(f"Quality: {product_details['quality']}\n")
            txt_file.write(f"Price: ${product_details['price']}\n\n")
            
            txt_file.write("Customer Information:\n")
            for key, value in checkout_info.items():
                txt_file.write(f"{key.replace('_', ' ').title()}: {value}\n")
        
        # Save CSV file
        with open(csv_filepath, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['pd_id', 'product_name', 'quality', 'price'])
            csv_writer.writerow([
                product_details['pd_id'], 
                product_details['product_name'], 
                product_details['quality'], 
                product_details['price']
            ])
            
            # Additional CSV rows for customer information
            csv_writer.writerow([])  # Empty row for separation
            csv_writer.writerow(['Customer Information'])
            for key, value in checkout_info.items():
                csv_writer.writerow([key, value])
        
        print(f"\nOrder saved. Order ID: {order_id}")
        print(f"Order details saved in {txt_filepath} and {csv_filepath}")

def kickoff():
    shop_flow = ShopFlow()
    shop_flow.kickoff()

def plot():
    shop_flow = ShopFlow()
    shop_flow.kickoff()