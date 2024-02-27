import tkinter as tk

#Add Vehicle
def add_vehicle(inventory):
    make = make_entry.get()
    model = model_entry.get()
    year = year_entry.get()
    mileage = mileage_entry.get()

    #Check if fields are empty
    if not (make and model and year and mileage):
        status_label.config(text="Please fill in all fields")
        return
    
    #Check if mileage is a valid float number
    try:
        mileage  = float(mileage)
    except ValueError:
        status_label.config(text="Please enter a valid mileage.")
        return
    
    #If checks pass, add vehicle to inventory
    vehicle = {
        "Make": make,
        "Model": model,
        "Year": year,
        "Mileage": mileage
    }

    inventory.append(vehicle)
    status_label.config(text="Vehicle added to inventory.")

def view_inventory_window(inventory):
    view_window = tk.Toplevel(root)
    view_window.title("View Inventory")

    if not inventory:
        tk.Label(view_window, text="Inventory is empty").pack()
    else:
        tk.Label(view_window, text="Current Inventory:").pack()
        for index, vehicle in enumerate(inventory, start=1):
            tk.Label(view_window, text=f"{index}. {vehicle['Year']} {vehicle['Make']} {vehicle['Model']} - Mileage: {vehicle['Mileage']}").pack()

def add_vehicle_window():
    add_window = tk.Toplevel(root)
    add_window.title("Add Vehicle")

    tk.Label(add_window, text="Year:").grid(row=0, column=0)
    tk.Label(add_window, text="Make:").grid(row=1, column=0)
    tk.Label(add_window, text="Model:").grid(row=2, column=0)
    tk.Label(add_window, text="Mileage:").grid(row=3, column=0)

    global make_entry, model_entry, year_entry, mileage_entry
    make_entry = tk.Entry(add_window)
    model_entry = tk.Entry(add_window)
    year_entry = tk.Entry(add_window)
    mileage_entry = tk.Entry(add_window)

    make_entry.grid(row=0, column=1)
    model_entry.grid(row=1, column=1)
    year_entry.grid(row=2, column=1)
    mileage_entry.grid(row=3, column=1)

    tk.Button(add_window, text="Add Vehicle", command=lambda: [add_vehicle(inventory), add_window.destroy()]).grid(row=4, column=0, columnspan=2)

root = tk.Tk()
root.title("Vehicle Inventory Management")

root.geometry("200x100")

inventory = []

status_label = tk.Label(root, text="")
status_label.pack()

add_button = tk.Button(root, text="Add Vehicle", command=add_vehicle_window)
add_button.pack()

view_button = tk.Button(root, text="View Inventory", command=lambda: view_inventory_window(inventory))
view_button.pack()

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack()

root.mainloop()
