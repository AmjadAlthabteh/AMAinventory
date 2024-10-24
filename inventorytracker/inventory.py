import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from style import Style

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏀 AMA League Inventory & Player Management 🏀")
        self.root.geometry("900x600")
        self.root.configure(bg=Style.BG_COLOR)

        # store teams and players in a dictionary
        self.teams = {}  # {team_name: [list_of_players]}

        # title and clock
        self.create_title_and_clock()

        # entry widgets and buttons
        self.create_entry_widgets()
        self.create_buttons()

        # team and player display section
        self.create_team_player_section()

    def create_title_and_clock(self):
        # title
        self.title_label = tk.Label(self.root, text="🏀 AMA League Inventory 🏀", font=Style.FONT_TITLE, bg=Style.BG_COLOR, fg=Style.HIGHLIGHT_COLOR)
        self.title_label.pack(pady=20)

        # clock
        self.clock_label = tk.Label(self.root, font=Style.FONT_CLOCK, bg=Style.BG_COLOR, fg=Style.TEXT_COLOR)
        self.clock_label.pack(pady=10)
        self.update_clock()

    def create_entry_widgets(self):
        # team entry
        self.team_label = tk.Label(self.root, text="Team Name", font=Style.FONT_LABEL, bg=Style.BG_COLOR, fg=Style.TEXT_COLOR)
        self.team_label.pack(pady=5)
        self.team_entry = tk.Entry(self.root, font=Style.FONT_ENTRY, bg=Style.ENTRY_BG, fg=Style.ENTRY_TEXT_COLOR, bd=0, relief="solid", width=25)
        self.team_entry.pack(pady=5, ipadx=30, ipady=10)

        # player entry
        self.player_label = tk.Label(self.root, text="Player Name", font=Style.FONT_LABEL, bg=Style.BG_COLOR, fg=Style.TEXT_COLOR)
        self.player_label.pack(pady=5)
        self.player_entry = tk.Entry(self.root, font=Style.FONT_ENTRY, bg=Style.ENTRY_BG, fg=Style.ENTRY_TEXT_COLOR, bd=0, relief="solid", width=25)
        self.player_entry.pack(pady=5, ipadx=30, ipady=10)

    def create_buttons(self):
        # add team button
        self.add_team_button = tk.Button(self.root, text="Add Team", font=Style.FONT_BUTTON, bg=Style.BUTTON_COLOR, fg="white", bd=0, command=self.add_team)
        self.add_team_button.pack(pady=10, ipadx=Style.BUTTON_PADX, ipady=Style.BUTTON_PADY)
        self.add_team_button.bind("<Enter>", self.on_enter)
        self.add_team_button.bind("<Leave>", self.on_leave)

        # add player button
        self.add_player_button = tk.Button(self.root, text="Add Player", font=Style.FONT_BUTTON, bg=Style.BUTTON_COLOR, fg="white", bd=0, command=self.add_player)
        self.add_player_button.pack(pady=10, ipadx=Style.BUTTON_PADX, ipady=Style.BUTTON_PADY)
        self.add_player_button.bind("<Enter>", self.on_enter)
        self.add_player_button.bind("<Leave>", self.on_leave)

    def create_team_player_section(self):
        # section for displaying teams and their players
        self.player_section_frame = tk.Frame(self.root, bg=Style.BG_COLOR)
        self.player_section_frame.pack(pady=10, side="right", fill="both", expand=True)

        self.player_section_label = tk.Label(self.player_section_frame, text="Teams & Players", font=Style.FONT_LABEL, bg=Style.BG_COLOR, fg=Style.HIGHLIGHT_COLOR)
        self.player_section_label.pack()

        self.player_text = tk.Text(self.player_section_frame, font=Style.FONT_ENTRY, bg=Style.ENTRY_BG, fg=Style.ENTRY_TEXT_COLOR, wrap="word", height=20, width=40)
        self.player_text.pack(pady=10, fill="both", expand=True)

    def add_team(self):
        team_name = self.team_entry.get()
        if team_name:
            if team_name not in self.teams:
                self.teams[team_name] = []  # initialize empty list of players
                self.display_teams_and_players()  # update display
                messagebox.showinfo("Success", f"Team '{team_name}' added!")
            else:
                messagebox.showerror("Error", "Team already exists!")
        else:
            messagebox.showerror("Error", "Please enter a team name.")

    def add_player(self):
        player_name = self.player_entry.get()
        team_name = self.team_entry.get()
        if player_name and team_name:
            if team_name in self.teams:
                self.teams[team_name].append(player_name)  # add player to selected team
                self.display_teams_and_players()  # update the player section
                messagebox.showinfo("Success", f"Player '{player_name}' added to team '{team_name}'!")
            else:
                messagebox.showerror("Error", f"Team '{team_name}' does not exist. Please add the team first.")
        else:
            messagebox.showerror("Error", "Please enter both a team name and a player name.")

    def display_teams_and_players(self):
        """display all teams and their players."""
        self.player_text.config(state="normal")
        self.player_text.delete(1.0, tk.END)  # clear the current text

        for team, players in self.teams.items():
            self.player_text.insert(tk.END, f"{team}:\n", "team_header")  # insert team name
            for player in players:
                self.player_text.insert(tk.END, f"  - {player}\n", "player_item")  # insert player names
            self.player_text.insert(tk.END, "\n")  # extra space between teams

        self.player_text.config(state="disabled")  # make text read-only

    def on_enter(self, event):
        event.widget.config(bg=Style.BUTTON_HOVER)  # hover effect for buttons

    def on_leave(self, event):
        event.widget.config(bg=Style.BUTTON_COLOR)

    def update_clock(self):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
                                        # I updated the code to make sure teams and players show up together in one section, with players listed under their respective teams.
                                        #  The style of the app is cleaner now, and everything works smoothly. Just focused on making it easier to use and making sure the display looks good.






