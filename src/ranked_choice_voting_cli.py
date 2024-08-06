import sys
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

def main():
    print("Welcome to the Ranked Choice Voting System!")
    
    candidates = get_candidates()
    if len(candidates) < 2:
        print("Error: At least two candidates are required.")
        return

    election = Election(candidates)
    
    ballots = get_ballots(candidates)
    for ballot in ballots:
        try:
            election.add_ballot(ballot)
        except InvalidBallotException as e:
            print(f"Invalid ballot: {e}")

    if not election.ballots:
        print("No valid ballots were submitted. Cannot run the election.")
        return

    print("\nRunning the election...")
    winner = election.run_election()
    
    print("\nElection Results:")
    election.print_results()
    print(f"\nThe winner is: {winner}")

if __name__ == "__main__":
    main()
