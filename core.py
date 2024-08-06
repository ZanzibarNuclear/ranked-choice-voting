from collections import defaultdict

class Candidate:
    def __init__(self, name):
        self.name = name
        self.eliminated = False

class Ballot:
    def __init__(self, rankings):
        self.rankings = rankings
        self.current_rank = 0

    def get_next_choice(self):
        while self.current_rank < len(self.rankings):
            candidate = self.rankings[self.current_rank]
            self.current_rank += 1
            if not candidate.eliminated:
                return candidate
        return None

    def has_more_choices(self):
        return self.current_rank < len(self.rankings)

class Round:
    def __init__(self, vote_counts, eliminated_candidate=None, is_tie=False):
        self.vote_counts = vote_counts
        self.eliminated_candidate = eliminated_candidate
        self.is_tie = is_tie

class Election:
    def __init__(self, candidates):
        self.candidates = {candidate.name: candidate for candidate in candidates}
        self.ballots = []
        self.rounds = []

    def add_ballot(self, rankings):
        ballot = Ballot([self.candidates[name] for name in rankings])
        self.ballots.append(ballot)

    def count_votes(self):
        counts = defaultdict(int)
        for ballot in self.ballots:
            choice = ballot.get_next_choice()
            if choice:
                counts[choice] += 1
        return counts

    def eliminate_candidates(self, candidates_to_eliminate):
        for candidate in candidates_to_eliminate:
            candidate.eliminated = True

    def is_tie(self, vote_counts):
        return len(set(vote_counts.values())) == 1 and len(vote_counts) > 1

    def any_ballots_have_more_choices(self):
        return any(ballot.has_more_choices() for ballot in self.ballots)

    def run_election(self):
        while True:
            vote_counts = self.count_votes()
            
            if not vote_counts:
                self.rounds.append(Round({}, is_tie=True))
                return "No winner"

            total_votes = sum(vote_counts.values())
            
            is_tie_round = self.is_tie(vote_counts)
            
            self.rounds.append(Round(vote_counts.copy(), is_tie=is_tie_round))
            
            if is_tie_round:
                if not self.any_ballots_have_more_choices():
                    return "No winner"
                print(f"Tie detected in round {len(self.rounds)}. Moving to next choices.")
                continue
            
            for candidate, votes in vote_counts.items():
                if votes > total_votes / 2:
                    return candidate.name

            min_votes = min(vote_counts.values())
            candidates_to_eliminate = [c for c, v in vote_counts.items() if v == min_votes]
            
            self.eliminate_candidates(candidates_to_eliminate)
            self.rounds[-1].eliminated_candidate = ", ".join([c.name for c in candidates_to_eliminate])
            
            remaining_candidates = [c for c in self.candidates.values() if not c.eliminated]
            if len(remaining_candidates) == 1:
                return remaining_candidates[0].name
            elif len(remaining_candidates) == 0:
                return "No winner"

    def print_results(self):
        for i, round in enumerate(self.rounds, 1):
            print(f"Round {i}:")
            for candidate, votes in round.vote_counts.items():
                print(f"  {candidate.name}: {votes}")
            if round.is_tie:
                print("  This round was a tie.")
                if i == len(self.rounds):
                    print("  No more choices available. Election ended in a tie.")
            elif round.eliminated_candidate:
                print(f"  Eliminated: {round.eliminated_candidate}")
            print()

def run_test(test_candidate_names, test_ballots, expected_winner):
    candidates = [Candidate(candidate_name) for candidate_name in test_candidate_names]
    election = Election(candidates)
    
    for ballot_ranking in test_ballots:
        election.add_ballot(ballot_ranking)
    
    winner = election.run_election()
    print(f"The result is: {winner}")
    election.print_results()
    
    passing_test = expected_winner == winner
    print(f"The test {'Passed' if passing_test else 'Failed'}\n************\n\n")
    
    return passing_test

# Test cases
def run_all_tests():
    tests = [
        {
            "name": "Simple Majority Winner",
            "candidates": ["Alice", "Bob", "Charlie"],
            "ballots": [
                ["Alice", "Bob", "Charlie"],
                ["Alice", "Charlie", "Bob"],
                ["Bob", "Alice", "Charlie"],
                ["Alice", "Bob", "Charlie"]
            ],
            "expected": "Alice"
        },
        {
            "name": "Runoff Required",
            "candidates": ["Alice", "Bob", "Charlie"],
            "ballots": [
                ["Alice", "Bob", "Charlie"],
                ["Bob", "Alice", "Charlie"],
                ["Charlie", "Alice", "Bob"],
                ["Charlie", "Bob", "Alice"]
            ],
            "expected": "Charlie"
        },
        {
            "name": "Tie Result",
            "candidates": ["Alice", "Bob", "Charlie", "David"],
            "ballots": [
                ["Alice", "Bob", "Charlie", "David"],
                ["Bob", "Charlie", "David", "Alice"],
                ["Charlie", "David", "Alice", "Bob"],
                ["David", "Alice", "Bob", "Charlie"]
            ],
            "expected": "No winner"
        }
    ]

    for test in tests:
        print(f"Running test: {test['name']}")
        result = run_test(test["candidates"], test["ballots"], test["expected"])
        if not result:
            print(f"Test failed: {test['name']}")
            return False
    
    print("All tests passed successfully!")
    return True

# Run all tests
run_all_tests()
