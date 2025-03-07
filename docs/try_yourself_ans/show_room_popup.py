##
# OTHER CODE ...
##

###################################################################
# This is the function to handles show_room_popup() 
# -----------------------------------------------------------------  
def show_room_popup(roomData, address):
    popup = tk.Toplevel(root)
    popup.title("Rooms Information")
    popup.geometry("700x300")
    popup.configure(bg="#f0f0f0")
    
    label = tk.Label(popup, text=f"Room data at {address}", font=("Arial", 12, "bold"), bg="#f0f0f0")
    label.pack(pady=(10, 5))
    
    table_frame = tk.Frame(popup, bg="#f0f0f0")
    table_frame.pack(pady=5, padx=10, fill="both", expand=True)
    table = ttk.Treeview(table_frame, show="headings", height=5)
    table.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    table.configure(yscrollcommand=scrollbar.set)
    
    # Handle case where roomData is not a list or is empty
    if not isinstance(roomData, list) or not roomData:
        table["columns"] = ("Message",)
        table.heading("Message", text="Message")
        table.column("Message", width=200, anchor="center")
        table.insert("", "end", values=("No room data available",))
        return
    
    # Dynamically define columns from the keys of the first room item
    first_roomData = roomData[0]
    if not isinstance(first_roomData, dict):
        table["columns"] = ("Message",)
        table.heading("Message", text="Message")
        table.column("Message", width=200, anchor="center")
        table.insert("", "end", values=("Invalid room data format",))
        return
    
    columns = list(first_roomData.keys())
    table["columns"] = columns
    for col in columns:
        table.heading(col, text=col.capitalize())
        table.column(col, width=100, anchor="w")  # Default width, adjustable
    
    # Populate table with room data
    for room in roomData:
        values = [str(room.get(col, "N/A")) for col in columns]
        table.insert("", "end", values=values)

##
# OTHER CODE ...
##

def show_response_table():
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
        ###################################################################
        # ADD thisstatement to trigger the show_room_popup() function call 
        # -----------------------------------------------------------------    
        if "room_data" in full_data and full_data["room_data"]:
            show_room_popup(full_data["room_data"], full_data["address"])


##
# OTHER CODE ...
##