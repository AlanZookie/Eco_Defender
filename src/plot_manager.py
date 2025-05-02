import random

class PlotManager:
    """
    Manages narrative sequences, user choices, and history review.
    Expects a dict of sequences passed in, e.g.:
      {
        'intro': {
          'lines': ["Text line 1", "Text line 2", ...],
          'choices': [
            {'text': "Choice A", 'next_seq': 'path_a'},
            {'text': "Choice B", 'next_seq': 'path_b'},
            {'text': "Choice C", 'next_seq': 'path_c'}
          ]
        },
        'path_a': {...},
        ...
      }
    """
    def __init__(self, sequences):
        self.sequences = sequences
        self.current_seq = 'intro'
        self.current_index = 0
        self.history = []
        self.available_events = [f'event_{i}' for i in range(1, 31)]  # List of all event IDs
        self.used_events = set()  # Track used events

    def get_current_text(self):
        """Return the current narrative line."""
        seq = self.sequences[self.current_seq]
        return seq['lines'][self.current_index]

    def advance(self):
        """
        Advance to next line. If at end and choices exist, return choices list.
        Otherwise, return None.
        """
        seq = self.sequences[self.current_seq]
        # Save to history
        self.history.append(self.get_current_text())

        # For bad ending, only show first line and then show choices
        if self.current_seq == 'bad_ending':
            if self.current_index < len(seq['lines']) - 1:
                self.current_index += 1
                return None
            else:
                return seq['choices']
            
        # For good ending, show all lines before showing choices
        if self.current_seq == 'good_ending':
            if self.current_index < len(seq['lines']) - 1:
                self.current_index += 1
                return None
            else:
                return seq['choices']

        # Check for branching
        if 'choices' in seq and self.current_index == len(seq['lines']) - 1:
            return seq['choices']

        # Move to next line
        self.current_index += 1
        # If exceeds, stay at last
        if self.current_index >= len(seq['lines']):
            self.current_index = len(seq['lines']) - 1
        return None

    def choose(self, choice_index):
        """
        Apply user choice, switch to next sequence, reset index.
        choice_index is 0-based.
        """
        if self.current_seq == 'intro':
            # Start the game and show first random event
            self.current_seq = self._get_next_random_event()
            self.current_index = 0
            return

        # For regular events, move to next random event after choice
        self.current_seq = self._get_next_random_event()
        self.current_index = 0

    def _get_next_random_event(self):
        """Get the next random event that hasn't been used yet"""
        if not self.available_events:
            # All events used, end game
            return 'end_game'

        # Select a random event that hasn't been used
        next_event = random.choice(self.available_events)
        self.available_events.remove(next_event)
        self.used_events.add(next_event)
        return next_event

    def review_history(self):
        """Return list of all displayed lines so far."""
        return list(self.history)
