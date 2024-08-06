import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from ranked_choice_voting import Candidate, Election, InvalidBallotException

class RankedChoiceVotingGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Ranked Choice Voting System")
        self.master.geometry("800x600")

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both")

        self.create_new_election_tab()
        self.load_existing_election_tab()
        self.save_election_tab()
        self.view_results_tab()

        self.election = None
        self.candidate_rankings = {}

    def create_new_election_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Create New Election")

        # Candidate section
        ttk.Label(tab, text="Add Candidates:").grid(row=0, column=0, padx=10, pady=5)
        self.candidate_entry = ttk.Entry(tab)
        self.candidate_entry.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(tab, text="Add Candidate", command=self.add_candidate).grid(row=0, column=2, padx=10, pady=5)

        self.candidates_frame = ttk.Frame(tab)
        self.candidates_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        # Ballot section
        ttk.Label(tab, text="Create Ballot:").grid(row=2, column=0, padx=10, pady=5)
        ttk.Button(tab, text="Submit Ballot", command=self.submit_ballot).grid(row=2, column=1, padx=10, pady=5)

        self.ballots_listbox = tk.Listbox(tab)
        self.ballots_listbox.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        ttk.Button(tab, text="Run Election", command=self.run_election).grid(row=4, column=1, padx=10, pady=5)

        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_rowconfigure(3, weight=1)

    def load_existing_election_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Load Existing Election")

        ttk.Button(tab, text="Select File", command=self.load_election).pack(pady=20)

    def save_election_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Save Election")

        ttk.Label(tab, text="Save current election:").pack(pady=20)
        ttk.Button(tab, text="Save Election", command=self.save_election).pack(pady=10)

        self.save_status = ttk.Label(tab, text="")
        self.save_status.pack(pady=10)

    def view_results_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="View Results")

        self.round_var = tk.StringVar()
        self.round_dropdown = ttk.Combobox(tab, textvariable=self.round_var, state="readonly")
        self.round_dropdown.pack(pady=10)
        self.round_dropdown.bind("<<ComboboxSelected>>", self.update_results_view)

        self.canvas = tk.Canvas(tab, bg="white")
        self.canvas.pack(expand=True, fill="both", padx=10, pady=10)

        self.info_text = tk.Text(tab, height=5, wrap=tk.WORD)
        self.info_text.pack(fill="x", padx=10, pady=10)

    def add_candidate(self):
        candidate = self.candidate_entry.get().strip()
        if candidate:
            if candidate in self.candidate_rankings:
                messagebox.showerror("Error", "This candidate already exists.")
                return
            self.candidate_rankings[candidate] = tk.StringVar()
            self.update_candidate_list()
            self.candidate_entry.delete(0, tk.END)

    def update_candidate_list(self):
        for widget in self.candidates_frame.winfo_children():
            widget.destroy()

        for i, (candidate, var) in enumerate(self.candidate_rankings.items()):
            ttk.Label(self.candidates_frame, text=candidate).grid(row=i, column=0, padx=5, pady=2)
            ranking_dropdown = ttk.Combobox(self.candidates_frame, textvariable=var, 
                                            values=list(range(1, len(self.candidate_rankings) + 1)), 
                                            state="readonly", width=5)
            ranking_dropdown.grid(row=i, column=1, padx=5, pady=2)
            ranking_dropdown.set("")  # Clear the initial selection

    def submit_ballot(self):
        rankings = {candidate: int(var.get()) if var.get() else float('inf') 
                    for candidate, var in self.candidate_rankings.items()}
        if not rankings or all(rank == float('inf') for rank in rankings.values()):
            messagebox.showerror("Error", "Please rank at least one candidate.")
            return
        sorted_ballot = sorted(rankings, key=rankings.get)
        self.ballots_listbox.insert(tk.END, ", ".join(sorted_ballot))
        for var in self.candidate_rankings.values():
            var.set("")  # Clear rankings after submission

    def run_election(self):
        if not self.candidate_rankings:
            messagebox.showerror("Error", "Please add candidates before running the election.")
            return
        if self.ballots_listbox.size() == 0:
            messagebox.showerror("Error", "Please add at least one ballot before running the election.")
            return

        candidates = [Candidate(c) for c in self.candidate_rankings.keys()]
        self.election = Election(candidates)

        for ballot in self.ballots_listbox.get(0, tk.END):
            try:
                self.election.add_ballot(ballot.split(', '))
            except InvalidBallotException as e:
                messagebox.showerror("Invalid Ballot", str(e))
                return

        winner = self.election.run_election()
        messagebox.showinfo("Election Result", f"The winner is: {winner}")
        self.update_results_view()

    def load_election(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                candidates = [Candidate(name) for name in data["candidates"]]
                self.election = Election(candidates)
                for ballot in data["ballots"]:
                    self.election.add_ballot(ballot)
                self.election.run_election()
                messagebox.showinfo("Election Loaded", "Election data loaded successfully")
                self.update_results_view()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load election: {str(e)}")

    def update_results_view(self, event=None):
        if not self.election or not self.election.rounds:
            return

        self.round_dropdown['values'] = [f"Round {i+1}" for i in range(len(self.election.rounds))]
        if not self.round_var.get():
            self.round_var.set(self.round_dropdown['values'][-1])

        round_index = int(self.round_var.get().split()[-1]) - 1
        round = self.election.rounds[round_index]

        self.canvas.delete("all")
        max_votes = max(round.vote_counts.values())
        bar_width = 30
        spacing = 10
        x_start = 50
        y_start = 20

        for i, (candidate, votes) in enumerate(round.vote_counts.items()):
            bar_height = (votes / max_votes) * 200 if max_votes > 0 else 0
            x = x_start + i * (bar_width + spacing)
            self.canvas.create_rectangle(x, y_start + 200 - bar_height, x + bar_width, y_start + 200, fill="blue")
            self.canvas.create_text(x + bar_width/2, y_start + 210, text=candidate.name, angle=90, anchor="w")
            self.canvas.create_text(x + bar_width/2, y_start + 190 - bar_height, text=str(votes), anchor="s")

        info = f"Round {round_index + 1}\n"
        if round.eliminated_candidate:
            info += f"Eliminated: {round.eliminated_candidate}\n"
        if round.is_tie:
            info += "This round was a tie.\n"
            if round.tie_broken:
                info += "Tie broken using next choice votes."

        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)

    def save_election(self):
        if not self.election:
            messagebox.showerror("Error", "No election to save. Please create or load an election first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json")])
        if not file_path:
            return  # User cancelled the save operation

        try:
            election_data = {
                "candidates": [candidate.name for candidate in self.election.candidates.values()],
                "ballots": [[candidate.name for candidate in ballot.rankings] for ballot in self.election.ballots]
            }

            with open(file_path, 'w') as f:
                json.dump(election_data, f, indent=2)

            self.save_status.config(text=f"Election saved successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save election: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RankedChoiceVotingGUI(root)
    root.mainloop()
