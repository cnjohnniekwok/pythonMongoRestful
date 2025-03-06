import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import json

# API base URL
API_URL = "http://localhost:5000/items"

# Main window
root = tk.Tk()
root.title("MongoDB CRUD UI")
root.geometry("700x500")
root.configure(bg="#f0f0f0")

# Frame for content
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# JSON Input Field
tk.Label(main_frame, text="JSON Input:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(0, 5))
json_input = tk.Text(main_frame, height=5, width=60, font=("Arial", 10), borderwidth=2, relief="groove")
json_input.pack(pady=5)

# Output Display
tk.Label(main_frame, text="Response:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(10, 5))
response_output = scrolledtext.ScrolledText(main_frame, height=10, width=60, font=("Arial", 10), borderwidth=2, relief="groove", bg="#ffffff")
response_output.pack(pady=5)

# Helper function to clear response
def clear_response():
    response_output.delete(1.0, tk.END)

# Helper function to display response
def display_response(response):
    clear_response()
    try:
        response_output.insert(tk.END, json.dumps(response.json(), indent=2))
    except:
        response_output.insert(tk.END, f"Error: {response.status_code}\n{response.text}")

# CRUD Functions
def create_item():
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        response = requests.post(API_URL, json=data)
        display_response(response)
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
        display_response(response)
        if response.status_code != 200:
            messagebox.showerror("Error", f"Failed: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")

def query_items():
    try:
        data = json.loads(json_input.get("1.0", tk.END).strip())
        response = requests.get(f"{API_URL}/query", json=data)
        display_response(response)
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
        display_response(response)
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
        display_response(response)
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
        display_response(response)
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
        display_response(response)
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
default_style = {"font": ("Arial", 10, "bold"), "width": 12, "height": 2, "relief": "raised", "bg": "#4CAF50", "fg": "white"}  # Green for Create, Read, Query
update_style = {"font": ("Arial", 10, "bold"), "width": 12, "height": 2, "relief": "raised", "bg": "#2196F3", "fg": "white"}   # Blue for Update, Bulk Update
delete_style = {"font": ("Arial", 10, "bold"), "width": 12, "height": 2, "relief": "raised", "bg": "#F44336", "fg": "white"}   # Red for Delete, Bulk Delete

# First row of buttons
tk.Button(button_frame, text="Create", command=create_item, **default_style).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Read All", command=read_items, **default_style).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Query", command=query_items, **default_style).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Update", command=update_item, **update_style).grid(row=0, column=3, padx=5, pady=5)

# Second row of buttons
tk.Button(button_frame, text="Delete", command=delete_item, **delete_style).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Bulk Update", command=bulk_update_items, **update_style).grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Bulk Delete", command=bulk_delete_items, **delete_style).grid(row=1, column=2, padx=5, pady=5)

# Start the application
root.mainloop()