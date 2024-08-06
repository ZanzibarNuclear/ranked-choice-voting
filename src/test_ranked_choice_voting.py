import pytest
from ranked_choice_voting import Candidate, Election, InvalidBallotException

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
            ["Dilbert", "Ted", "Wally", "Alice"],
            ["Dilbert", "Ted", "Alice", "Wally"],
            ["Alice", "Ted", "Wally", "Dilbert"],
            ["Alice", "Ted", "Dilbert", "Wally"],
            ["Wally", "Ted", "Alice", "Dilbert"],
            ["Wally", "Ted", "Dilbert", "Alice"],
        ],
        "expected": "Ted"
    }
])
def test_ranked_choice_voting(test_case):
    winner, election = run_election(test_case["candidates"], test_case["ballots"])
    
    print(f"\nRunning test: {test_case['name']}")
    print(f"The result is: {winner}")
    election.print_results()
    
    assert winner == test_case["expected"], f"Expected {test_case['expected']}, but got {winner}"

def test_empty_ballot():
    election = Election([Candidate("Alice"), Candidate("Bob")])
    with pytest.raises(InvalidBallotException, match="Ballot is empty"):
        election.add_ballot([])

def test_duplicate_candidates():
    election = Election([Candidate("Alice"), Candidate("Bob"), Candidate("Charlie")])
    with pytest.raises(InvalidBallotException, match="Ballot contains duplicate candidates"):
        election.add_ballot(["Alice", "Bob", "Alice"])

def test_invalid_candidate():
    election = Election([Candidate("Alice"), Candidate("Bob")])
    with pytest.raises(InvalidBallotException, match="Invalid candidate: Charlie"):
        election.add_ballot(["Alice", "Charlie"])

def test_incomplete_ballot(capsys):
    election = Election([Candidate("Alice"), Candidate("Bob"), Candidate("Charlie")])
    election.add_ballot(["Alice", "Bob"])
    captured = capsys.readouterr()
    assert "Warning: Ballot has fewer candidates than registered (2 < 3)" in captured.out

def test_valid_ballot():
    election = Election([Candidate("Alice"), Candidate("Bob"), Candidate("Charlie")])
    election.add_ballot(["Alice", "Bob", "Charlie"])
    assert len(election.ballots) == 1

def test_no_valid_ballots():
    election = Election([Candidate("Alice"), Candidate("Bob")])
    result = election.run_election()
    assert result == "No winner"
