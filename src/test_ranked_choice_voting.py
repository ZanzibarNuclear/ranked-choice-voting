import pytest
from ranked_choice_voting import Candidate, Election

def run_election(candidates, ballots):
    election = Election([Candidate(name) for name in candidates])
    for ballot in ballots:
        election.add_ballot(ballot)
    winner = election.run_election()
    return winner, election

@pytest.mark.parametrize("test_case", [
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
        "candidates": ["Dilbert", "Alice", "Wally", "Dave"],
        "ballots": [
            ["Dilbert", "Alice", "Dave", "Wally"],
            ["Dilbert", "Alice", "Dave", "Wally"],
            ["Alice", "Wally", "Dilbert", "Dave"],
            ["Alice", "Wally", "Dilbert", "Dave"],
            ["Dave", "Dilbert", "Alice", "Wally"],
            ["Dave", "Dilbert", "Alice", "Wally"],
            ["Dave", "Alice", "Wally", "Dilbert"],
            ["Wally", "Dilbert", "Dave", "Alice"]
        ],
        "expected": "Dilbert"
    },
    {
        "name": "Tie-breaking with second choice votes",
        "candidates": ["Dilbert", "Alice", "Wally", "Ted"],
        "ballots": [
            ["Dilbert", "Alice", "Wally", "Ted"],
            ["Alice", "Dilbert", "Wally", "Ted"],
            ["Wally", "Dilbert", "Alice", "Ted"],
            ["Wally", "Alice", "Dilbert", "Ted"],
            ["Dilbert", "Ted", "Alice", "Wally"],
        ],
        "expected": "Dilbert"
    }
])
def test_ranked_choice_voting(test_case):
    winner, election = run_election(test_case["candidates"], test_case["ballots"])
    
    print(f"\nRunning test: {test_case['name']}")
    print(f"The result is: {winner}")
    election.print_results()
    
    assert winner == test_case["expected"], f"Expected {test_case['expected']}, but got {winner}"

def test_invalid_ballot():
    with pytest.raises(KeyError):
        run_election(["Dilbert", "Alice"], [["Dilbert", "Wally"]])

def test_empty_election():
    winner, _ = run_election(["Dilbert", "Alice"], [])
    assert winner == "No winner"

def test_single_candidate():
    winner, _ = run_election(["Dilbert"], [["Dilbert"]])
    assert winner == "Dilbert"
