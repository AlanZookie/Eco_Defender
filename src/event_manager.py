import random
import time
from src.stats_manager import StatsManager

class EventManager:
    def __init__(self):
        self.stats = StatsManager()
        self.event_history = []
        self.game_started = False
        self.last_update = time.time()
        self.updates_paused = False
        
        # Set initial values
        self.stats.set('pollution', 0.5)  # 50%
        self.stats.set('deforestation', 0.4)  # 40%
    
    def start_game(self):
        """Start the game and begin tracking values"""
        self.game_started = True
        self.last_update = time.time()
        self.event_history.append("Game started - Beginning environmental tracking")
    
    def pause_updates(self):
        """Pause the event manager updates"""
        self.updates_paused = True
        self.last_update = time.time()  # Reset the last update time

    def resume_updates(self):
        """Resume the event manager updates"""
        self.updates_paused = False
        self.last_update = time.time()  # Reset the last update time

    def update(self):
        """Update environmental values based on time"""
        if not self.game_started or self.updates_paused:
            return

        current_time = time.time()
        time_diff = current_time - self.last_update
        
        # Get current values
        current_pollution = self.stats.get('pollution')
        current_deforestation = self.stats.get('deforestation')
        
        # Only update if values haven't reached good ending conditions
        if current_pollution > 0.15:  # 15%
            pollution_increase = 0.01 * time_diff  # 1% per second
            self.stats.set('pollution', min(1.0, current_pollution + pollution_increase))
            
        if current_deforestation > 0.15:  # 15%
            deforestation_increase = 0.007 * time_diff  # 1% per second
            self.stats.set('deforestation', min(1.0, current_deforestation + deforestation_increase))
        
        self.last_update = current_time
    
    def apply_choice_effect(self, choice_id):
        """Apply effects based on player's choice"""
        if not self.game_started:
            if choice_id == 'begin_journey':
                self.start_game()
            return
            
        # Define standard effects based on event type and choice position
        pollution_effects = {
            0: -0.2,  # First choice: -20%
            1: -0.1,  # Second choice: -10%
            2: 0.05   # Third choice: +5%
        }
        
        deforestation_effects = {
            0: -0.15,  # First choice: -15%
            1: -0.1,   # Second choice: -10%
            2: 0.05    # Third choice: +5%
        }
        
        # Determine if this is a pollution or deforestation event
        # and which choice was made (0, 1, or 2)
        choice_index = int(choice_id.split('_')[-1]) if choice_id.split('_')[-1].isdigit() else 0
        
        # Apply effects based on event type
        if 'pollution' in choice_id or any(keyword in choice_id for keyword in ['energy', 'recycling', 'water', 'noise', 'chemicals', 'heat', 'traffic', 'plastics', 'air', 'waste']):
            effect = pollution_effects.get(choice_index, 0)
            self.stats.adjust('pollution', effect)
            self.event_history.append(f"Choice: {choice_id} - Pollution effect: {effect}")
            
        elif 'deforestation' in choice_id or any(keyword in choice_id for keyword in ['trees', 'forest', 'logging', 'land', 'habitat', 'green', 'buffer']):
            effect = deforestation_effects.get(choice_index, 0)
            self.stats.adjust('deforestation', effect)
            self.event_history.append(f"Choice: {choice_id} - Deforestation effect: {effect}")
    
    def get_current_values(self):
        """Get current values of all environmental factors"""
        if not self.game_started:
            return {
                'pollution': 0.5,  # 50%
                'deforestation': 0.4,  # 40%
            }
        return {
            'pollution': self.stats.get('pollution'),
            'deforestation': self.stats.get('deforestation'),
        }
    
    def get_event_history(self):
        """Get history of events and their effects"""
        return self.event_history
    
    def reset_values(self):
        """Reset all values to initial state"""
        self.stats.set('pollution', 0.5)  # Reset to 50%
        self.stats.set('deforestation', 0.4)  # Reset to 40%
        self.event_history = []
        self.game_started = False
        self.last_update = time.time() 