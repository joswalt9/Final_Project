import os
import tkinter as tk
from tkinter import ttk
import json
import datetime

add_vehicle_image = None # Set variable for add.png
view_vehicle_image = None # Set variable for view.png
logo_image = None # Set variable for logo.png

# Get the directory where the script resides
script_dir = os.path.dirname(os.path.abspath(__file__))

# Function to save inventory to a file
def save_inventory(inventory):
    with open(os.path.join(script_dir, "inventory.json"), "w") as file:
        json.dump(inventory, file)

# Function to load inventory to a file
def load_inventory():
    try:
        with open(os.path.join(script_dir, "inventory.json"), "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
# Function to handle program exit
def on_exit():
    save_inventory(inventory)
    root.destroy()

# Function to delete a vehicle from inventory
def delete_vehicle(index, view_window):
    del inventory[index] # Delete Vehicle
    save_inventory(inventory) # Save inventory
    view_window.destroy() # Close inventory window
    view_inventory_window(inventory) # Reload inventory window
    status_label.config(text="Vehicle deleted from inventory.") # Update status label

# Function to check if Stock Number has been used previously
def is_stock_number_used(stock, inventory):
    for vehicle in inventory:
        if vehicle['Stock'] == stock:
            return True
    return False

# Function to check if VIN has been used previously
def is_vin_used(vin, inventory):
    for vehicle in inventory:
        if vehicle['VIN'] == vin:
            return True
    return False

# Add Vehicle Function
def add_vehicle(inventory):
    # Get user input
    stock = stock_entry.get()
    make = make_entry.get()
    model = model_entry.get()
    year = year_entry.get()
    mileage = mileage_entry.get()
    vin = vin_entry.get()

    # Check if fields are empty
    if not (stock and make and model and year and mileage and vin):
        status_label.config(text="Please fill in all fields") # Update status label
        return
    
    # Check if Stock Number has been entered previously
    if is_stock_number_used(stock, inventory):
        status_label.config(text=f"Stock # has been used previously") # Update status label
        return

    # Check if Year is valid
    try:
        year = int(year)
        today = datetime.date.today() # Find current date
        current_year = today.year # Find current year
        car_year = current_year + 1 # Add 1 to current year 
        if year < 1888 or year > car_year:
            raise ValueError
    except ValueError:
        status_label.config(text="Please enter a valid year. Ex 1900-" + str(car_year)) # Update status label
        return
    
    # Check if mileage is a valid float number
    try:
        mileage  = float(mileage)
    except ValueError:
        status_label.config(text="Please enter a valid mileage.") # Update status label
        return
    
    # Check if VIN has been entered previously
    if is_vin_used(vin, inventory):
        status_label.config(text=f"VIN has been used previously") # Update status label
        return
    
    #Check if VIN number is 16 characters long
    if len(vin) != 16:
        status_label.config(text="VIN must be exactly 16 characters long.") # Update status label
    
    # If checks pass, add vehicle to inventory
    vehicle = {
        "Stock": stock,
        "Make": make,
        "Model": model,
        "Year": year,
        "Mileage": mileage,
        "VIN": vin
    }

    inventory.append(vehicle) # Add vehicle to inventory
    save_inventory(inventory) # Save Inventory
    status_label.config(text="Vehicle added to inventory.") # Update status label

# Function to display seperate inventory window
def view_inventory_window(inventory):
    global view_vehicle_image

    # Sort inventory by stock number
    inventory.sort(key=lambda x: x['Stock'])

    # Function to refresh inventory window
    def refresh():
        view_window.destroy()
        view_inventory_window(inventory)

    # Create a new window to display inventory
    view_window = tk.Toplevel(root)
    view_window.title("View Inventory")

    # Display view.png
    try:
        view_vehicle_image = tk.PhotoImage(file=os.path.join(script_dir, "view.png"))
        image_label = tk.Label(view_window, image=view_vehicle_image)
        image_label.pack()
    except tk.TclError:
        tk.Label(view_window, text="View Inventory").pack() # Display alternate text if view.png fails to load.

    # Check if inventory is empty
    if not inventory:
        tk.Label(view_window, text="Inventory is empty").pack()
    else:
        # Display vehicle inventory
        for index, vehicle in enumerate(inventory, start=1):
            # Create a frame
            frame = tk.Frame(view_window, bd=1, relief="solid") # Add a border
            frame.pack(fill="x", padx=2, pady=2)

            vehicle_label = tk.Label(frame, text=f"{vehicle['Stock']}. {vehicle['Year']} {vehicle['Make']} {vehicle['Model']} - Mileage: {vehicle['Mileage']} - VIN: {vehicle['VIN']}")
            vehicle_label.pack(side="left")
            # Add delete button to each entry
            delete_button = tk.Button(frame, text="Delete", command=lambda idx=index-1, window=view_window: delete_vehicle(idx, view_window))
            delete_button.pack(side="right")

    # Button to refresh inventory display
    refresh_button = tk.Button(view_window, text="Refresh", command=refresh)
    refresh_button.pack()

# Function to display 'Add Vehicle' window
def add_vehicle_window():
    global add_vehicle_image

    # Create a new window for adding a vehicle
    add_window = tk.Toplevel(root)
    add_window.title("Add Vehicle")

    # Display add.png
    try:
        add_vehicle_image = tk.PhotoImage(file=os.path.join(script_dir, "add.png"))
        image_label = tk.Label(add_window, image=add_vehicle_image)
        image_label.grid(row=0, column=0, columnspan=2)
    except:
        tk.Label(add_window, text="Add Vehicle").grid(row=0, column=0, columnspan=2) # Display alternate text if add.png fails to load.

    # Labels and entry fields for data input
    tk.Label(add_window, text="Stock:").grid(row=1, column=0)
    tk.Label(add_window, text="Year:").grid(row=2, column=0)
    tk.Label(add_window, text="Make:").grid(row=3, column=0)
    tk.Label(add_window, text="Model:").grid(row=4, column=0)
    tk.Label(add_window, text="Mileage:").grid(row=5, column=0)
    tk.Label(add_window, text="VIN:").grid(row=6, column=0)

    # Entry fields for user input
    global stock_entry, make_entry, model_entry, year_entry, mileage_entry, vin_entry
    stock_entry = tk.Entry(add_window) #Entry field for stock number 
    year_entry = tk.Entry(add_window) #Entry field for year
    make_entry = tk.Entry(add_window) #Entry field for make
    model_entry = tk.Entry(add_window) #Entry field for model
    mileage_entry = tk.Entry(add_window) #Entry field for mileage
    vin_entry = tk.Entry(add_window) #Entry field for VIN

    # Position entry fields in the window
    stock_entry.grid(row=1, column=1)
    year_entry.grid(row=2, column=1)
    make_entry.grid(row=3, column=1)
    model_entry.grid(row=4, column=1)
    mileage_entry.grid(row=5, column=1)
    vin_entry.grid(row=6, column=1)

    # Button to add vehicle and close window
    tk.Button(add_window, text="Add Vehicle", command=lambda: [add_vehicle(inventory), add_window.destroy()]).grid(row=7, column=0, columnspan=2)

    # Limit characters to 20 in Make and Model fields
    make_entry.config(validate="key", validatecommand=(make_entry.register(validate_make_model), "%P"))
    model_entry.config(validate="key", validatecommand=(model_entry.register(validate_make_model), "%P"))

    # Limit characters to 16 in VIN field
    vin_entry.config(validate="key", validatecommand=(vin_entry.register(validate_vin), "%P"))

# Validation function to limit character length in Make and Model fields
def validate_make_model(new_text):
    return len(new_text) <= 20  # Limiting to 20 characters

# Validation function to limit character length in VIN field
def validate_vin(new_text):
    return len(new_text) <= 16 # Limiting to 16 characters

# Main Tkinter Window
root = tk.Tk()
root.title("Inventory Control")

# Display logo.png
try:
    logo_image = tk.PhotoImage(file=os.path.join(script_dir, "logo.png"))
    label = ttk.Label(image=logo_image)
    label.pack()
except tk.TclError:
    ttk.Label(text="Inventory Control").pack() # Display alternate text if logo.png fails to load.

root.geometry("210x160") # Set window size for main window

inventory = load_inventory() # Load inventory

status_label = tk.Label(root, text="") # Create status label
status_label.pack()

add_button = tk.Button(root, text="Add Vehicle", command=add_vehicle_window) # Create Add Vehicle Button
add_button.pack()

view_button = tk.Button(root, text="View Inventory", command=lambda: view_inventory_window(inventory)) # Create View Inventory Button
view_button.pack()

exit_button = tk.Button(root, text="Exit", command=lambda: [save_inventory(inventory), root.quit()])  # Call save_inventory() before quitting
exit_button.pack()

root.mainloop()
