import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
import requests
import json

# API base URL
API_URL = "http://localhost:5000/items"

# Main window
root = tk.Tk()
root.title("MongoDB CRUD UI")
root.geometry("900x700")
root.configure(bg="#f0f0f0")

# Frame for content
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

# Table Response Output
tk.Label(main_frame, text="Response Table:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(10, 5))
table_frame = tk.Frame(main_frame, bg="#f0f0f0")
table_frame.pack(pady=5, fill="both", expand=True)
table = ttk.Treeview(table_frame, show="headings", height=5)
table.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
table.configure(yscrollcommand=scrollbar.set)

# Helper function to clear outputs
def clear_outputs():
    response_output.delete(1.0, tk.END)
    curl_output.delete(1.0, tk.END)
    for item in table.get_children():
        table.delete(item)

# Helper function to generate cURL command
def generate_curl(method, url, data=None):
    cmd = f"curl -X {method} \"{url}\""
    if data:
        cmd += f" -H \"Content-Type: application/json\" -d '{json.dumps(data)}'"
    return cmd

# Helper function to display response in table
def display_table(response):
    for item in table.get_children():
        table.delete(item)
    try:
        data = response.json()
        if isinstance(data, list):  # Handle array response (e.g., Read All, Query)
            if not data:
                table["columns"] = ("Message",)
                table.heading("Message", text="Message")
                table.column("Message", width=200, anchor="center")
                table.insert("", "end", values=("No items found",))
                return
            # Get all unique keys from the first item
            keys = list(data[0].keys())
            table["columns"] = keys
            for key in keys:
                table.heading(key, text=key.capitalize())
                table.column(key, width=100, anchor="w")
            for item in data:
                values = [str(item.get(key, "")) for key in keys]
                table.insert("", "end", values=values)
        elif isinstance(data, dict):  # Handle single object response (e.g., Create, Update)
            if "error" in data or "message" in data or "id" in data or "deleted_count" in data:
                table["columns"] = ("Key", "Value")
                table.heading("Key", text="Key")
                table.heading("Value", text="Value")
                table.column("Key", width=100, anchor="w")
                table.column("Value", width=200, anchor="w")
                for key, value in data.items():
                    table.insert("", "end", values=(key.capitalize(), str(value)))
            else:  # Single item response
                keys = list(data.keys())
                table["columns"] = keys
                for key in keys:
                    table.heading(key, text=key.capitalize())
                    table.column(key, width=100, anchor="w")
                values = [str(data.get(key, "")) for key in keys]
                table.insert("", "end", values=values)
    except:
        table["columns"] = ("Message",)
        table.heading("Message", text="Message")
        table.column("Message", width=200, anchor="center")
        table.insert("", "end", values=(f"Error: {response.status_code} - {response.text}",))

# CRUD Functions
def create_item():
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        response = requests.post(API_URL, json=data)
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("POST", API_URL, data))
        display_table(response)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Item created successfully!")
        else:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON input")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def read_items():
    try:
        response = requests.get(API_URL)
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("GET", API_URL))
        display_table(response)
        if response.status_code != 200:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def query_items():
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        response = requests.get(f"{API_URL}/query", json=data)
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("GET", f"{API_URL}/query", data))
        display_table(response)
        if response.status_code == 200:
            messagebox.showinfo("Success", f"Found {len(response.json())} items")
        else:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON input")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def update_item():
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        if "_id" not in data:
            messagebox.showerror("Error", "JSON must include '_id' for update")
            return
        item_id = data.pop("_id")
        response = requests.put(f"{API_URL}/{item_id}", json=data)
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("PUT", f"{API_URL}/{item_id}", data))
        display_table(response)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Item updated successfully!")
        else:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON input")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def bulk_update_items():
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        if "query" not in data or "update" not in data:
            messagebox.showerror("Error", "JSON must include 'query' and 'update' fields")
            return
        response = requests.put(f"{API_URL}/bulk-update", json=data)
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("PUT", f"{API_URL}/bulk-update", data))
        display_table(response)
        if response.status_code == 200:
            messagebox.showinfo("Success", f"Bulk update completed: {response.json()['modified_count']} items modified")
        else:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON input")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def delete_item():
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        if "_id" not in data:
            messagebox.showerror("Error", "JSON must include '_id' for delete")
            return
        item_id = data["_id"]
        response = requests.delete(f"{API_URL}/{item_id}")
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("DELETE", f"{API_URL}/{item_id}"))
        display_table(response)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Item deleted successfully!")
        else:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON input")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def bulk_delete_items():
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        if "query" not in data:
            messagebox.showerror("Error", "JSON must include 'query' field")
            return
        response = requests.delete(f"{API_URL}/bulk-delete", json=data)
        clear_outputs()
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
        curl_output.insert(tk.END, generate_curl("DELETE", f"{API_URL}/bulk-delete", data))
        display_table(response)
        if response.status_code == 200:
            messagebox.showinfo("Success", f"Bulk delete completed: {response.json()['deleted_count']} items deleted")
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

# First row of buttons (Create, Read All, Query)
tk.Button(button_frame, text="Create", command=create_item, **default_style).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Read All", command=read_items, **default_style).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Query", command=query_items, **default_style).grid(row=0, column=2, padx=5, pady=5)

# Second row of buttons (Update, Delete, Bulk Update, Bulk Delete)
tk.Button(button_frame, text="Update", command=update_item, **update_style).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Delete", command=delete_item, **delete_style).grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Bulk Update", command=bulk_update_items, **update_style).grid(row=1, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Bulk Delete", command=bulk_delete_items, **delete_style).grid(row=1, column=3, padx=5, pady=5)

# Start the application
root.mainloop()