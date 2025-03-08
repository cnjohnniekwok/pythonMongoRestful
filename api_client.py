import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
import requests
import json
from PIL import Image, ImageTk
import io
import base64

# API base URL
API_URL = "http://localhost:5000/properties"

# Main window
root = tk.Tk()
root.title("MongoDB CRUD UI")
root.geometry("700x600")
root.configure(bg="#f0f0f0")

# Frame for content (full window since no image frame)
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# JSON Input Field
tk.Label(main_frame, text="JSON Input:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(0, 5))
json_input = tk.Text(main_frame, height=5, width=80, font=("Arial", 10), borderwidth=2, relief="groove")
json_input.pack(pady=5)

# Raw Response Output
tk.Label(main_frame, text="Raw Response:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(10, 5))
response_output = scrolledtext.ScrolledText(main_frame, height=5, width=80, font=("Arial", 10), borderwidth=2, relief="groove", bg="#ffffff")
response_output.pack(pady=5)

# Postman/cURL Command Output
tk.Label(main_frame, text="Postman/cURL Command:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(10, 5))
curl_output = scrolledtext.ScrolledText(main_frame, height=3, width=80, font=("Arial", 10), borderwidth=2, relief="groove", bg="#ffffff")
curl_output.pack(pady=5)

# Store full data for the popup table
row_data = {}
latest_response = None  # To store the latest response for the popup

# Helper function to clear outputs
def clear_outputs():
    response_output.delete(1.0, tk.END)
    curl_output.delete(1.0, tk.END)
    row_data.clear()

# Helper function to generate cURL command
def generate_curl(method, url, data=None):
    cmd = f"curl -X {method} \"{url}\""
    if data:
        cmd += f" -H \"Content-Type: application/json\" -d '{json.dumps(data)}'"
    return cmd

# Helper function to show image in a popup
def show_image_popup(image_data, address):
    popup = tk.Toplevel(root)
    popup.title("Image Display")
    popup.geometry("300x350")
    popup.configure(bg="#f0f0f0")
    
    label = tk.Label(popup, text=address, font=("Arial", 12, "bold"), bg="#f0f0f0")
    label.pack(pady=(10, 5))
    image_label = tk.Label(popup, bg="#ffffff", borderwidth=2, relief="groove")
    image_label.pack(pady=5)
    
    try:
        img_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(img_bytes))
        img = img.resize((250, 250), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        image_label.configure(image=photo)
        image_label.image = photo  # Keep reference
    except Exception as e:
        image_label.configure(text=f"Error loading image: {str(e)}")
        print(f"Image error: {str(e)}")

def show_gardens_popup(gardens, address):
    popup = tk.Toplevel(root)
    popup.title("Gardens Information")
    popup.geometry("400x300")
    popup.configure(bg="#f0f0f0")
    
    label = tk.Label(popup, text=f"Gardens at {address}", font=("Arial", 12, "bold"), bg="#f0f0f0")
    label.pack(pady=(10, 5))
    
    table_frame = tk.Frame(popup, bg="#f0f0f0")
    table_frame.pack(pady=5, padx=10, fill="both", expand=True)
    table = ttk.Treeview(table_frame, show="headings", height=5)
    table.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    table.configure(yscrollcommand=scrollbar.set)
    
    # Handle case where gardens is not a list or is empty
    if not isinstance(gardens, list) or not gardens:
        table["columns"] = ("Message",)
        table.heading("Message", text="Message")
        table.column("Message", width=200, anchor="center")
        table.insert("", "end", values=("No garden data available",))
        return
    
    # Dynamically define columns from the keys of the first garden item
    first_garden = gardens[0]
    if not isinstance(first_garden, dict):
        table["columns"] = ("Message",)
        table.heading("Message", text="Message")
        table.column("Message", width=200, anchor="center")
        table.insert("", "end", values=("Invalid room data format",))
        return
    
    columns = list(first_garden.keys())
    table["columns"] = columns
    for col in columns:
        table.heading(col, text=col.capitalize())
        table.column(col, width=100, anchor="w")  # Default width, adjustable
    
    # Populate table with garden data
    for garden in gardens:
        values = [str(garden.get(col, "N/A")) for col in columns]
        table.insert("", "end", values=values)

# Helper function to create and populate the response table popup
def show_response_table():
    global latest_response
    if latest_response is None:
        messagebox.showinfo("Info", "No response data available. Perform an action first.")
        return

    # Create popup window for table
    popup = tk.Toplevel(root)
    popup.title("Response Table")
    popup.geometry("800x400")
    popup.configure(bg="#f0f0f0")

    # Table frame in popup
    table_frame = tk.Frame(popup, bg="#f0f0f0")
    table_frame.pack(pady=10, padx=10, fill="both", expand=True)
    table = ttk.Treeview(table_frame, show="headings", height=10)
    table.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    table.configure(yscrollcommand=scrollbar.set)

    # Populate table with latest response
    try:
        data = latest_response.json()
        if isinstance(data, list):  # Handle array response
            if not data:
                table["columns"] = ("Message",)
                table.heading("Message", text="Message")
                table.column("Message", width=200, anchor="center")
                table.insert("", "end", values=("No properties found",))
            else:
                keys = list(data[0].keys())
                table["columns"] = keys
                for key in keys:
                    table.heading(key, text=key.capitalize())
                    table.column(key, width=100 if key != "image" else 200, anchor="w")
                for item in data:
                    values = [str(item.get(key, ""))[:50] if key == "image" else str(item.get(key, "")) for key in keys]
                    row_id = table.insert("", "end", values=values)
                    row_data[row_id] = item
        elif isinstance(data, dict):  # Handle single object response
            if "error" in data or "message" in data or "id" in data or "deleted_count" in data:
                table["columns"] = ("Key", "Value")
                table.heading("Key", text="Key")
                table.heading("Value", text="Value")
                table.column("Key", width=100, anchor="w")
                table.column("Value", width=200, anchor="w")
                for key, value in data.items():
                    table.insert("", "end", values=(key.capitalize(), str(value)))
            else:
                keys = list(data.keys())
                table["columns"] = keys
                for key in keys:
                    table.heading(key, text=key.capitalize())
                    table.column(key, width=100 if key != "image" else 200, anchor="w")
                values = [str(data.get(key, ""))[:50] if key == "image" else str(data.get(key, "")) for key in keys]
                row_id = table.insert("", "end", values=values)
                row_data[row_id] = data
    except:
        table["columns"] = ("Message",)
        table.heading("Message", text="Message")
        table.column("Message", width=200, anchor="center")
        table.insert("", "end", values=(f"Error: {latest_response.status_code} - {latest_response.text}",))

    # Bind click event to show image popup if image exists
    def handle_row_click(event):
        selected = table.selection()
        if not selected:
            return
        row_id = selected[0]
        full_data = row_data.get(row_id, {})
        print(f"Selected row full data: {full_data}")  # Debug print
        if "image" in full_data and full_data["image"]:
            show_image_popup(full_data["image"],full_data["address"])
        if "gardens" in full_data and full_data["gardens"]:
            show_gardens_popup(full_data["gardens"], full_data["address"])

    table.bind("<ButtonRelease-1>", handle_row_click)

# CRUD Functions
def create_item():
    global latest_response
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        response = requests.post(API_URL, json=data)
        latest_response = response
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("POST", API_URL, data))
        if response.status_code == 201:
            messagebox.showinfo("Success", "Item created successfully!")
        else:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON input")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def read_properties():
    global latest_response
    try:
        response = requests.get(API_URL)
        latest_response = response
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("GET", API_URL))
        if response.status_code != 200:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def query_properties():
    global latest_response
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        response = requests.get(f"{API_URL}/query", json=data)
        latest_response = response
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("GET", f"{API_URL}/query", data))
        if response.status_code == 200:
            messagebox.showinfo("Success", f"Found {len(response.json())} properties")
        else:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON input")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def update_item():
    global latest_response
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        if "_id" not in data:
            messagebox.showerror("Error", "JSON must include '_id' for update")
            return
        item_id = data.pop("_id")
        response = requests.put(f"{API_URL}/{item_id}", json=data)
        latest_response = response
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("PUT", f"{API_URL}/{item_id}", data))
        if response.status_code == 200:
            messagebox.showinfo("Success", "Item updated successfully!")
        else:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON input")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def bulk_update_properties():
    global latest_response
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        if "query" not in data or "update" not in data:
            messagebox.showerror("Error", "JSON must include 'query' and 'update' fields")
            return
        response = requests.put(f"{API_URL}/bulk-update", json=data)
        latest_response = response
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("PUT", f"{API_URL}/bulk-update", data))
        if response.status_code == 200:
            messagebox.showinfo("Success", f"Bulk update completed: {response.json()['modified_count']} properties modified")
        else:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON input")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def delete_item():
    global latest_response
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        if "_id" not in data:
            messagebox.showerror("Error", "JSON must include '_id' for delete")
            return
        item_id = data["_id"]
        response = requests.delete(f"{API_URL}/{item_id}")
        latest_response = response
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("DELETE", f"{API_URL}/{item_id}"))
        if response.status_code == 200:
            messagebox.showinfo("Success", "Item deleted successfully!")
        else:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON input")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def bulk_delete_properties():
    global latest_response
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        if "query" not in data:
            messagebox.showerror("Error", "JSON must include 'query' field")
            return
        response = requests.delete(f"{API_URL}/bulk-delete", json=data)
        latest_response = response
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("DELETE", f"{API_URL}/bulk-delete", data))
        if response.status_code == 200:
            messagebox.showinfo("Success", f"Bulk delete completed: {response.json()['deleted_count']} properties deleted")
        else:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON input")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

# Buttons Frame with two rows
button_frame = tk.Frame(main_frame, bg="#f0f0f0")
button_frame.pack(pady=10)

# Button styles
default_style = {"font": ("Arial", 10, "bold"), "width": 12, "height": 2, "relief": "raised", "bg": "#4CAF50", "fg": "white"}
update_style = {"font": ("Arial", 10, "bold"), "width": 12, "height": 2, "relief": "raised", "bg": "#2196F3", "fg": "white"}
delete_style = {"font": ("Arial", 10, "bold"), "width": 12, "height": 2, "relief": "raised", "bg": "#F44336", "fg": "white"}
table_style = {"font": ("Arial", 10, "bold"), "width": 12, "height": 2, "relief": "raised", "bg": "#FFC107", "fg": "black"}

# First row of buttons (Create, Read All, Query, Show Table)
tk.Button(button_frame, text="Create", command=create_item, **default_style).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Read All", command=read_properties, **default_style).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Query", command=query_properties, **default_style).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Show Table", command=show_response_table, **table_style).grid(row=0, column=3, padx=5, pady=5)

# Second row of buttons (Update, Delete, Bulk Update, Bulk Delete)
tk.Button(button_frame, text="Update", command=update_item, **update_style).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Delete", command=delete_item, **delete_style).grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Bulk Update", command=bulk_update_properties, **update_style).grid(row=1, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Bulk Delete", command=bulk_delete_properties, **delete_style).grid(row=1, column=3, padx=5, pady=5)

# Start the application
root.mainloop()