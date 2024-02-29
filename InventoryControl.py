import tkinter as tk
from tkinter import ttk

add_vehicle_image = None #Set variable for add.png
view_vehicle_image = None #Set variable for view.png
logo_image = None #Set variable for logo.png

#Add Vehicle Function
def add_vehicle(inventory):
    #Get user input
    make = make_entry.get()
    model = model_entry.get()
    year = year_entry.get()
    mileage = mileage_entry.get()

    #Check if fields are empty
    if not (make and model and year and mileage):
        status_label.config(text="Please fill in all fields") #Update status label
        return
    
    #Check if Year is valid
    try:
        year = int(year)
        current_year = 2024 
        if year < 1900 or year > current_year:
            raise ValueError
    except ValueError:
        status_label.config(text="Please enter a valid year.") #Update status label
        return
    
    #Check if mileage is a valid float number
    try:
        mileage  = float(mileage)
    except ValueError:
        status_label.config(text="Please enter a valid mileage.") #Update status label
        return
    
    #If checks pass, add vehicle to inventory
    vehicle = {
        "Make": make,
        "Model": model,
        "Year": year,
        "Mileage": mileage
    }

    inventory.append(vehicle) #Add vehicle to inventory
    status_label.config(text="Vehicle added to inventory.") #Update status label

#Function to display seperate inventory window
def view_inventory_window(inventory):
    global view_vehicle_image

    #Function to refresh inventory window
    def refresh():
        view_window.destroy()
        view_inventory_window(inventory)

    #Create a new window to display inventory
    view_window = tk.Toplevel(root)
    view_window.title("View Inventory")

    #Display view.png
    try:
        view_vehicle_image = tk.PhotoImage(file="view.png")
        image_label = tk.Label(view_window, image=view_vehicle_image)
        image_label.pack()
    except tk.TclError:
        tk.Label(view_window, text="View Inventory").pack()


    #Check if inventory is empty
    if not inventory:
        tk.Label(view_window, text="Inventory is empty").pack()
    else:
        #Display vehicle inventory
        for index, vehicle in enumerate(inventory, start=1):
            tk.Label(view_window, text=f"{index}. {vehicle['Year']} {vehicle['Make']} {vehicle['Model']} - Mileage: {vehicle['Mileage']}").pack()
    
    #Button to refresh inventory display
    refresh_button = tk.Button(view_window, text="Refresh", command=refresh)
    refresh_button.pack()

#Function to display 'Add Vehicle' window
def add_vehicle_window():
    global add_vehicle_image

    #Create a new window for adding a vehicle
    add_window = tk.Toplevel(root)
    add_window.title("Add Vehicle")

    #Display add.png
    try:
        add_vehicle_image = tk.PhotoImage(file="add.png")
        image_label = tk.Label(add_window, image=add_vehicle_image)
        image_label.grid(row=0, column=0, columnspan=2)
    except:
        tk.Label(add_window, text="Add Vehicle").grid(row=0, column=0, columnspan=2)

    #Labels and entry fields for data input
    tk.Label(add_window, text="Year:").grid(row=1, column=0)
    tk.Label(add_window, text="Make:").grid(row=2, column=0)
    tk.Label(add_window, text="Model:").grid(row=3, column=0)
    tk.Label(add_window, text="Mileage:").grid(row=4, column=0)

    #Entry fields for user input
    global make_entry, model_entry, year_entry, mileage_entry
    year_entry = tk.Entry(add_window) #Entry field for year
    make_entry = tk.Entry(add_window) #Entry field for make
    model_entry = tk.Entry(add_window) #Entry field for model
    mileage_entry = tk.Entry(add_window) #Entry field for mileage

    #Position entry fields in the window
    year_entry.grid(row=1, column=1)
    make_entry.grid(row=2, column=1)
    model_entry.grid(row=3, column=1)
    mileage_entry.grid(row=4, column=1)

    #Button to add vehicle and close window
    tk.Button(add_window, text="Add Vehicle", command=lambda: [add_vehicle(inventory), add_window.destroy()]).grid(row=5, column=0, columnspan=2)

#Main Tkinter Window
root = tk.Tk()
root.title("Inventory Control")

#Display logo.png
try:
    logo_image = tk.PhotoImage(file="logo.png")
    label = ttk.Label(image=logo_image)
    label.pack()
except tk.TclError:
    ttk.Label(text="Inventory Control").pack()

root.geometry("200x150")

inventory = [
    {"Year": "2022", "Make": "Toyota", "Model": "Camry", "Mileage": 25000},
    {"Year": "2024", "Make": "Toyota", "Model": "Avalon", "Mileage": 16000},
]

status_label = tk.Label(root, text="")
status_label.pack()

add_button = tk.Button(root, text="Add Vehicle", command=add_vehicle_window)
add_button.pack()

view_button = tk.Button(root, text="View Inventory", command=lambda: view_inventory_window(inventory))
view_button.pack()

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack()

root.mainloop()
