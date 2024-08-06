import sys
import json
from ranked_choice_voting import Candidate, Election, InvalidBallotException

def get_candidates():
    candidates = []
    print("Enter candidate names (enter an empty line when finished):")
    while True:
        name = input("Candidate name: ").strip()
        if not name:
            break
        candidates.append(Candidate(name))
    return candidates

def get_ballots(candidates):
    ballots = []
    candidate_names = [c.name for c in candidates]
    print("\nEnter ballots (enter an empty line when finished):")
    print("Format: Comma-separated list of candidates in order of preference")
    print(f"Available candidates: {', '.join(candidate_names)}")
    while True:
        ballot_input = input("Ballot: ").strip()
        if not ballot_input:
            break
        ballot = [name.strip() for name in ballot_input.split(',')]
        ballots.append(ballot)
    return ballots

def save_election(election, filename):
    data = {
        "candidates": [c.name for c in election.candidates.values()],
        "ballots": [[c.name for c in ballot.rankings] for ballot in election.ballots]
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Election data saved to {filename}")

def load_election(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    candidates = [Candidate(name) for name in data["candidates"]]
    election = Election(candidates)
    
    for ballot in data["ballots"]:
        try:
            election.add_ballot(ballot)
        except InvalidBallotException as e:
            print(f"Warning: Invalid ballot in saved data: {e}")
    
    return election

def main():
    print("Welcome to the Ranked Choice Voting System!")
    
    while True:
        print("\nChoose an option:")
        print("1. Create a new election")
        print("2. Load an existing election")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            candidates = get_candidates()
            if len(candidates) < 2:
                print("Error: At least two candidates are required.")
                continue

            election = Election(candidates)
            
            ballots = get_ballots(candidates)
            for ballot in ballots:
                try:
                    election.add_ballot(ballot)
                except InvalidBallotException as e:
                    print(f"Invalid ballot: {e}")

            if not election.ballots:
                print("No valid ballots were submitted. Cannot run the election.")
                continue
        
        elif choice == '2':
            filename = input("Enter the filename to load from: ").strip()
            try:
                election = load_election(filename)
                print(f"Election loaded from {filename}")
            except FileNotFoundError:
                print(f"Error: File {filename} not found.")
                continue
            except json.JSONDecodeError:
                print(f"Error: File {filename} is not a valid JSON file.")
                continue
        
        elif choice == '3':
            print("Thank you for using the Ranked Choice Voting System. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        print("\nRunning the election...")
        winner = election.run_election()
        
        print("\nElection Results:")
        election.print_results()
        print(f"\nThe winner is: {winner}")

        save_choice = input("\nDo you want to save this election? (y/n): ").strip().lower()
        if save_choice == 'y':
            filename = input("Enter a filename to save to: ").strip()
            save_election(election, filename)

if __name__ == "__main__":
    main()
