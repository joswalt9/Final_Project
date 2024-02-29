import os
import tkinter as tk
from tkinter import ttk
import json

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
    status_label.config(text="Vehicle deleted from inventory.") #Update status label

# Add Vehicle Function
def add_vehicle(inventory):
    # Get user input
    make = make_entry.get()
    model = model_entry.get()
    year = year_entry.get()
    mileage = mileage_entry.get()

    # Check if fields are empty
    if not (make and model and year and mileage):
        status_label.config(text="Please fill in all fields") # Update status label
        return
    
    # Check if Year is valid
    try:
        year = int(year)
        current_year = 2024 
        if year < 1900 or year > current_year:
            raise ValueError
    except ValueError:
        status_label.config(text="Please enter a valid year.") # Update status label
        return
    
    # Check if mileage is a valid float number
    try:
        mileage  = float(mileage)
    except ValueError:
        status_label.config(text="Please enter a valid mileage.") # Update status label
        return
    
    # If checks pass, add vehicle to inventory
    vehicle = {
        "Make": make,
        "Model": model,
        "Year": year,
        "Mileage": mileage
    }

    inventory.append(vehicle) # Add vehicle to inventory
    save_inventory(inventory) # Save Inventory
    status_label.config(text="Vehicle added to inventory.") # Update status label

# Function to display seperate inventory window
def view_inventory_window(inventory):
    global view_vehicle_image

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
            frame = tk.Frame(view_window)
            frame.pack(fill="x")

            vehicle_label = tk.Label(frame, text=f"{index}. {vehicle['Year']} {vehicle['Make']} {vehicle['Model']} - Mileage: {vehicle['Mileage']}")
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
    tk.Label(add_window, text="Year:").grid(row=1, column=0)
    tk.Label(add_window, text="Make:").grid(row=2, column=0)
    tk.Label(add_window, text="Model:").grid(row=3, column=0)
    tk.Label(add_window, text="Mileage:").grid(row=4, column=0)

    # Entry fields for user input
    global make_entry, model_entry, year_entry, mileage_entry
    year_entry = tk.Entry(add_window) #Entry field for year
    make_entry = tk.Entry(add_window) #Entry field for make
    model_entry = tk.Entry(add_window) #Entry field for model
    mileage_entry = tk.Entry(add_window) #Entry field for mileage

    # Position entry fields in the window
    year_entry.grid(row=1, column=1)
    make_entry.grid(row=2, column=1)
    model_entry.grid(row=3, column=1)
    mileage_entry.grid(row=4, column=1)

    # Button to add vehicle and close window
    tk.Button(add_window, text="Add Vehicle", command=lambda: [add_vehicle(inventory), add_window.destroy()]).grid(row=5, column=0, columnspan=2)

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

root.geometry("200x150") # Set window size for main window

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
