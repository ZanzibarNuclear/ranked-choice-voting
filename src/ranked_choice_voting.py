from collections import defaultdict

class InvalidBallotException(Exception):
    pass

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

    def get_second_choice(self):
        if len(self.rankings) > 1:
            return self.rankings[1]
        return None

class Round:
    def __init__(self, vote_counts, eliminated_candidate=None, is_tie=False, tie_broken=False):
        self.vote_counts = vote_counts
        self.eliminated_candidate = eliminated_candidate
        self.is_tie = is_tie
        self.tie_broken = tie_broken

class Election:
    def __init__(self, candidates):
        self.candidates = {candidate.name: candidate for candidate in candidates}
        self.ballots = []
        self.rounds = []

    def validate_ballot(self, rankings):
        if not rankings:
            raise InvalidBallotException("Ballot is empty")

        if len(rankings) != len(set(rankings)):
            raise InvalidBallotException("Ballot contains duplicate candidates")

        for candidate in rankings:
            if candidate not in self.candidates:
                raise InvalidBallotException(f"Invalid candidate: {candidate}")

        if len(rankings) < len(self.candidates):
            print(f"Warning: Ballot has fewer candidates than registered ({len(rankings)} < {len(self.candidates)})")

    def add_ballot(self, rankings):
        ballot = Ballot([self.candidates[name] for name in rankings])
        self.ballots.append(ballot)

    def count_votes(self):
        counts = {candidate: 0 for candidate in self.candidates.values() if not candidate.eliminated}
        for ballot in self.ballots:
            choice = ballot.get_next_choice()
            if choice:
                counts[choice] += 1
        return counts

    def count_next_choice_votes(self, candidates_to_check):
        next_choice_counts = defaultdict(int)
        for ballot in self.ballots:
            for choice in ballot.rankings[1:]:  # Start from the second choice
                if choice in candidates_to_check and not choice.eliminated:
                    next_choice_counts[choice] += 1
                    break
        return next_choice_counts

    def eliminate_candidate(self, candidate):
        candidate.eliminated = True
        # Reset all ballots to allow recounting
        for ballot in self.ballots:
            ballot.current_rank = 0

    def is_tie(self, vote_counts):
        return len(set(vote_counts.values())) == 1 and len(vote_counts) > 1

    def run_election(self):
        while True:
            vote_counts = self.count_votes()
            
            if not vote_counts:
                self.rounds.append(Round({}, is_tie=True))
                return "No winner"

            total_votes = sum(vote_counts.values())
            
            self.rounds.append(Round(vote_counts.copy()))
            
            # Check for a winner
            for candidate, votes in vote_counts.items():
                if votes > total_votes / 2:
                    return candidate.name

            # Check for a tie
            if self.is_tie(vote_counts):
                tied_candidates = list(vote_counts.keys())
                next_choice_counts = self.count_next_choice_votes(self.candidates.values())
                
                if next_choice_counts:
                    max_next_choices = max(next_choice_counts.values())
                    winners = [c for c, v in next_choice_counts.items() if v == max_next_choices]
                    
                    if len(winners) == 1:
                        self.rounds[-1].is_tie = True
                        self.rounds[-1].tie_broken = True
                        return winners[0].name

                self.rounds[-1].is_tie = True
                return "No winner"

            # Eliminate the candidate(s) with the least votes
            min_votes = min(vote_counts.values())
            candidates_to_eliminate = [c for c, v in vote_counts.items() if v == min_votes]
            
            for candidate in candidates_to_eliminate:
                self.eliminate_candidate(candidate)
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
                if round.tie_broken:
                    print("  Tie broken using second choice votes.")
                elif i == len(self.rounds):
                    print("  No more choices available. Election ended in a tie.")
            elif round.eliminated_candidate:
                print(f"  Eliminated: {round.eliminated_candidate}")
            print()

__all__ = ['Candidate', 'Ballot', 'Round', 'Election', 'InvalidBallotException']
