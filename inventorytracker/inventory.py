import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Style Configuration
BG_GRADIENT = "#1C2833"  # Darker background color
TEXT_COLOR = "#ECF0F1"  # Light text color
ENTRY_BG = "#2E4053"  # Darker gray for entry background
ENTRY_TEXT_COLOR = "#ECF0F1"  # Light text color for entries
BOX_COLOR = "#1ABC9C"  # Turquoise color for input field borders
BUTTON_BG = "#2980B9"  # Cool blue for buttons
BUTTON_HOVER_BG = "#1F618D"  # Darker blue for hover state
HIGHLIGHT_COLOR = "#F39C12"  # Rich orange color for highlights
LABEL_COLOR = "#D5D8DC"  # Softer light color for labels

TITLE_FONT_LARGE = ("Arial Black", 28, "bold")
LABEL_FONT = ("Arial", 14, "bold")
ENTRY_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 14, "bold")
CLOCK_FONT = ("Arial Black", 16)


class Player:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Equipment:
    def __init__(self, name, quantity=0, condition="N/A"):
        self.name = name
        self.quantity = quantity
        self.condition = condition

    def update(self, quantity, condition):
        self.quantity = quantity
        self.condition = condition

    def __str__(self):
        return f"{self.name} - Quantity: {self.quantity}, Condition: {self.condition}"


class Team:
    def __init__(self, name):
        self.name = name
        self.equipment = {}
        self.players = []

    def add_equipment(self, equipment_name, quantity, condition):
        if equipment_name in self.equipment:
            self.equipment[equipment_name].update(quantity, condition)
        else:
            self.equipment[equipment_name] = Equipment(equipment_name, quantity, condition)

    def add_player(self, player_name):
        self.players.append(Player(player_name))

    def view_inventory(self):
        inventory_text = f"{self.name} Inventory:\n"
        for equipment in self.equipment.values():
            inventory_text += str(equipment) + "\n"
        return inventory_text if inventory_text.strip() != f"{self.name} Inventory:" else f"{self.name} has no equipment."

    def view_roster(self):
        if not self.players:
            return f"{self.name} has no players."
        roster_text = f"{self.name} Roster:\n"
        for player in self.players:
            roster_text += str(player) + "\n"
        return roster_text


class League:
    def __init__(self, league_name):
        self.league_name = league_name
        self.teams = {}

    def add_team(self, team_name):
        if team_name not in self.teams:
            self.teams[team_name] = Team(team_name)
        else:
            messagebox.showinfo("Error", f"{team_name} already exists in the league.")

    def update_team_equipment(self, team_name, equipment_name, quantity, condition):
        if team_name in self.teams:
            self.teams[team_name].add_equipment(equipment_name, quantity, condition)
        else:
            messagebox.showinfo("Error", f"{team_name} does not exist in the league. Please add the team first.")

    def add_player_to_team(self, team_name, player_name):
        if team_name in self.teams:
            self.teams[team_name].add_player(player_name)
        else:
            messagebox.showinfo("Error", f"{team_name} does not exist in the league. Please add the team first.")

    def view_team_inventory(self, team_name):
        if team_name in self.teams:
            return self.teams[team_name].view_inventory()
        else:
            messagebox.showinfo("Error", f"{team_name} does not exist in the league.")

    def view_team_roster(self, team_name):
        if team_name in self.teams:
            return self.teams[team_name].view_roster()
        else:
            messagebox.showinfo("Error", f"{team_name} does not exist in the league.")


# GUI Application with Player Selection Feature
class InventoryApp:
    def __init__(self, root):
        self.league = League("American Muslim Athletes (AMA) League")
        self.root = root
        self.root.title("🏀 AMA League Inventory & Player Management 🏀")
        self.root.geometry("900x600")
        self.root.configure(bg=BG_GRADIENT)

        # Title and Clock Section
        self.title_frame = tk.Frame(root, bg=BG_GRADIENT)
        self.title_frame.pack(fill="x")

        # Title Label with Bigger Basketball Icon and Cool Color
        self.title_label = tk.Label(self.title_frame, text="🏀 AMA League Inventory & Player Management 🏀", font=TITLE_FONT_LARGE, bg=BG_GRADIENT, fg=HIGHLIGHT_COLOR)
        self.title_label.pack(pady=20, side="left", padx=20)

        # Clock Display
        self.clock_label = tk.Label(self.title_frame, font=CLOCK_FONT, bg=BG_GRADIENT, fg=LABEL_COLOR)
        self.clock_label.pack(side="right", padx=20)
        self.update_clock()

        # Entry Widgets
        self.create_entry_widget("Team Name:", "team")
        self.create_entry_widget("Player Name:", "player")
        self.create_entry_widget("Equipment Name:", "equipment")
        self.create_entry_widget("Quantity:", "quantity")
        self.create_entry_widget("Condition:", "condition")

        # Buttons
        self.add_team_button = tk.Button(root, text="Add Team", font=BUTTON_FONT, bg=BUTTON_BG, fg="white", command=self.add_team, bd=0, relief="flat")
        self.add_team_button.pack(pady=10, ipadx=10, ipady=5)
        self.add_team_button.bind("<Enter>", self.on_enter)
        self.add_team_button.bind("<Leave>", self.on_leave)

        self.add_player_button = tk.Button(root, text="Add Player to Team", font=BUTTON_FONT, bg=BUTTON_BG, fg="white", command=self.add_player, bd=0, relief="flat")
        self.add_player_button.pack(pady=10, ipadx=10, ipady=5)
        self.add_player_button.bind("<Enter>", self.on_enter)
        self.add_player_button.bind("<Leave>", self.on_leave)

        # Team List Section
        self.team_list_frame = tk.Frame(root, bg=BG_GRADIENT)
        self.team_list_frame.pack(side="right", fill="y", padx=20, pady=20)

        self.team_list_label = tk.Label(self.team_list_frame, text="Teams", font=LABEL_FONT, bg=BG_GRADIENT, fg=TEXT_COLOR)
        self.team_list_label.pack()

        self.team_listbox = tk.Listbox(self.team_list_frame, font=ENTRY_FONT, bg=ENTRY_BG, fg=ENTRY_TEXT_COLOR, selectbackground=BOX_COLOR, width=30, height=15)
        self.team_listbox.pack(pady=10)

        self.view_inventory_button = tk.Button(self.team_list_frame, text="View Inventory", font=BUTTON_FONT, bg=BUTTON_BG, fg="white", command=self.view_inventory, bd=0, relief="flat")
        self.view_inventory_button.pack(pady=5, ipadx=10, ipady=5)
        self.view_inventory_button.bind("<Enter>", self.on_enter)
        self.view_inventory_button.bind("<Leave>", self.on_leave)

        self.view_roster_button = tk.Button(self.team_list_frame, text="View Roster", font=BUTTON_FONT, bg=BUTTON_BG, fg="white", command=self.view_roster, bd=0, relief="flat")
        self.view_roster_button.pack(pady=5, ipadx=10, ipady=5)
        self.view_roster_button.bind("<Enter>", self.on_enter)
        self.view_roster_button.bind("<Leave>", self.on_leave)

    def create_entry_widget(self, label_text, entry_attr):
        label = tk.Label(self.root, text=label_text, font=LABEL_FONT, bg=BG_GRADIENT, fg=LABEL_COLOR)
        label.pack(pady=5)

        entry_box = tk.Frame(self.root, bg=BOX_COLOR)
        entry_box.pack_propagate(False)
        entry_box.pack(pady=5)
        entry_box.config(width=250, height=30)

        entry = tk.Entry(entry_box, font=ENTRY_FONT, bg=ENTRY_BG, fg=ENTRY_TEXT_COLOR, insertbackground=ENTRY_TEXT_COLOR, bd=0, relief="flat")
        entry.pack(fill="both", expand=True, padx=5, pady=5)

        setattr(self, f"{entry_attr}_entry", entry)

    def add_team(self):
        team_name = self.team_entry.get()
        if team_name:
            self.league.add_team(team_name)
            messagebox.showinfo("Success", f"Team '{team_name}' added successfully!")
            self.team_listbox.insert(tk.END, team_name)
        else:
            messagebox.showinfo("Error", "Please enter a team name.")
    
    def add_player(self):
        team_name = self.team_entry.get()
        player_name = self.player_entry.get()
        if team_name and player_name:
            self.league.add_player_to_team(team_name, player_name)
            messagebox.showinfo("Success", f"Player '{player_name}' added to team '{team_name}'!")
        else:
            messagebox.showinfo("Error", "Please enter both team and player names.")

    def view_inventory(self):
        selected_team = self.team_listbox.get(tk.ACTIVE)
        if selected_team:
            inventory = self.league.view_team_inventory(selected_team)
            messagebox.showinfo(f"{selected_team} Inventory", inventory)
        else:
            messagebox.showinfo("Error", "Please select a team.")

    def view_roster(self):
        selected_team = self.team_listbox.get(tk.ACTIVE)
        if selected_team:
            roster = self.league.view_team_roster(selected_team)
            messagebox.showinfo(f"{selected_team} Roster", roster)
        else:
            messagebox.showinfo("Error", "Please select a team.")

    def on_enter(self, event):
        event.widget.config(bg=BUTTON_HOVER_BG)

    def on_leave(self, event):
        event.widget.config(bg=BUTTON_BG)

    def update_clock(self):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)  # Update the clock every second


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

