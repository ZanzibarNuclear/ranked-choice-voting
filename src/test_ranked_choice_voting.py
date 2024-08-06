from ranked_choice_voting import Candidate, Election

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

def run_all_tests():
    tests = [
        {
            "name": "Simple Majority Winner",
            "candidates": ["Dilbert", "Alice", "Wally"],
            "ballots": [
                ["Dilbert", "Alice", "Wally"],
                ["Dilbert", "Wally", "Alice"],
                ["Alice", "Dilbert", "Wally"],
                ["Dilbert", "Alice", "Wally"]
            ],
            "expected": "Dilbert"
        },
        {
            "name": "Tie for biggest losers",
            "candidates": ["Dilbert", "Alice", "Wally"],
            "ballots": [
                ["Dilbert", "Alice", "Wally"],
                ["Alice", "Dilbert", "Wally"],
                ["Wally", "Dilbert", "Alice"],
                ["Wally", "Alice", "Dilbert"]
            ],
            "expected": "Wally"
        },
        {
            "name": "Tie all the way",
            "candidates": ["Dilbert", "Alice", "Wally", "Dave"],
            "ballots": [
                ["Dilbert", "Alice", "Wally", "Dave"],
                ["Alice", "Wally", "Dave", "Dilbert"],
                ["Wally", "Dave", "Dilbert", "Alice"],
                ["Dave", "Dilbert", "Alice", "Wally"]
            ],
            "expected": "No winner"
        },
        {
            "name": "Complex multi-round election",
            "candidates": ["Dilbert", "Alice", "Wally", "Dave", "Ashok"],
            "ballots": [
                ["Dilbert", "Alice", "Ashok", "Dave", "Wally"],
                ["Dilbert", "Alice", "Ashok", "Dave", "Wally"],
                ["Alice", "Wally", "Dave", "Dilbert", "Ashok"],
                ["Alice", "Wally", "Dilbert", "Dave", "Ashok"],
                ["Dave", "Dilbert", "Alice", "Wally", "Ashok"],
                ["Dave", "Dilbert", "Alice", "Wally", "Ashok"],
                ["Dave", "Ashok", "Alice", "Wally", "Dilbert"],
                ["Wally", "Dilbert", "Dave", "Alice", "Ashok"]
            ],
            "expected": "Dave"
        },
        {
            "name": "Tie-breaking with second choice votes",
            "candidates": ["Dilbert", "Alice", "Wally", "Ted"],
            "ballots": [
                ["Dilbert", "Alice", "Wally", "Ted"],
                ["Alice", "Dilbert", "Wally", "Ted"],
                ["Wally", "Dilbert", "Alice", "Ted"],
                ["Wally", "Alice", "Dilbert", "Ted"],
                ["Ted", "Dilbert", "Alice", "Wally"],
            ],
            "expected": "Dilbert"
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

if __name__ == "__main__":
    run_all_tests()