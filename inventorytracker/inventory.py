import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from style import Style


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title(" AMA League Inventory & Player Management 🏀")
        self.root.geometry("1000x650")
        self.root.configure(bg=Style.BG_COLOR)

        self.teams = {}   # {team: [players]}

        self.create_header()
        self.create_input_section()
        self.create_buttons()
        self.create_display_section()

    # ---------------- HEADER ----------------
    def create_header(self):
        header_frame = tk.Frame(self.root, bg=Style.BG_COLOR)
        header_frame.pack(pady=15)

        tk.Label(
            header_frame,
            text=" AMA League Inventory 🏀",
            font=Style.FONT_TITLE,
            bg=Style.BG_COLOR,
            fg=Style.HIGHLIGHT_COLOR
        ).pack()

        self.clock_label = tk.Label(
            header_frame,
            font=Style.FONT_CLOCK,
            bg=Style.BG_COLOR,
            fg=Style.TEXT_COLOR
        )
        self.clock_label.pack(pady=5)

        self.update_clock()

    # ---------------- INPUT SECTION ----------------
    def create_input_section(self):
        input_frame = tk.Frame(self.root, bg=Style.BG_COLOR)
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="Team Name", font=Style.FONT_LABEL,
                 bg=Style.BG_COLOR, fg=Style.TEXT_COLOR).grid(row=0, column=0, padx=10, pady=5)
        self.team_entry = tk.Entry(
            input_frame,
            font=Style.FONT_ENTRY,
            bg=Style.ENTRY_BG,
            fg=Style.ENTRY_TEXT_COLOR,
            width=28,
            bd=0,
            relief="solid"
        )
        self.team_entry.grid(row=1, column=0, padx=10, ipadx=20, ipady=10)

        tk.Label(input_frame, text="Player Name", font=Style.FONT_LABEL,
                 bg=Style.BG_COLOR, fg=Style.TEXT_COLOR).grid(row=0, column=1, padx=10, pady=5)
        self.player_entry = tk.Entry(
            input_frame,
            font=Style.FONT_ENTRY,
            bg=Style.ENTRY_BG,
            fg=Style.ENTRY_TEXT_COLOR,
            width=28,
            bd=0,
            relief="solid"
        )
        self.player_entry.grid(row=1, column=1, padx=10, ipadx=20, ipady=10)

    # ---------------- BUTTON SECTION ----------------
    def create_buttons(self):
        btn_frame = tk.Frame(self.root, bg=Style.BG_COLOR)
        btn_frame.pack(pady=10)

        self.add_team_button = self.make_button(
            btn_frame, "Add Team", self.add_team)
        self.add_team_button.grid(row=0, column=0, padx=20)

        self.add_player_button = self.make_button(
            btn_frame, "Add Player", self.add_player)
        self.add_player_button.grid(row=0, column=1, padx=20)

    def make_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=Style.FONT_BUTTON,
            bg=Style.BUTTON_COLOR,
            fg="white",
            bd=0,
            width=15,
            height=2
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=Style.BUTTON_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=Style.BUTTON_COLOR))
        return btn

    # ---------------- DISPLAY SECTION ----------------
    def create_display_section(self):
        frame = tk.Frame(self.root, bg=Style.BG_COLOR)
        frame.pack(fill="both", expand=True, padx=20, pady=15)

        tk.Label(
            frame,
            text="Teams & Players",
            font=Style.FONT_LABEL,
            bg=Style.BG_COLOR,
            fg=Style.HIGHLIGHT_COLOR
        ).pack(pady=5)

        text_frame = tk.Frame(frame, bg=Style.BG_COLOR)
        text_frame.pack(fill="both", expand=True)

        self.player_text = tk.Text(
            text_frame,
            font=Style.FONT_ENTRY,
            bg=Style.ENTRY_BG,
            fg=Style.ENTRY_TEXT_COLOR,
            wrap="word",
            state="disabled"
        )
        self.player_text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.player_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.player_text.config(yscrollcommand=scrollbar.set)

    # ---------------- LOGIC ----------------
    def add_team(self):
        team = self.team_entry.get().strip()
        if not team:
            messagebox.showerror("Error", "Please enter a team name.")
            return
        if team in self.teams:
            messagebox.showerror("Error", "Team already exists!")
            return

        self.teams[team] = []
        self.display_teams_and_players()
        messagebox.showinfo("Success", f"Team '{team}' added!")

    def add_player(self):
        player = self.player_entry.get().strip()
        team = self.team_entry.get().strip()

        if not player or not team:
            messagebox.showerror(
                "Error", "Please enter both a team name and a player name.")
            return

        if team not in self.teams:
            messagebox.showerror("Error", "Team does not exist!")
            return

        self.teams[team].append(player)
        self.display_teams_and_players()
        messagebox.showinfo(
            "Success", f"Player '{player}' added to '{team}'!")

    def display_teams_and_players(self):
        self.player_text.config(state="normal")
        self.player_text.delete(1.0, tk.END)

        for team, players in self.teams.items():
            self.player_text.insert(tk.END, f"{team}:\n")
            for p in players:
                self.player_text.insert(tk.END, f"  • {p}\n")
            self.player_text.insert(tk.END, "\n")

        self.player_text.config(state="disabled")

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
