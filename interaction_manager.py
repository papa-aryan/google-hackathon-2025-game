import pygame

RESET_BUFFER = 2 # Pixels to move away before an interaction can be reset

class InteractionManager:
    def __init__(self):
        self.interactables = []
        # Stores {interactable_id: has_interacted_bool}
        self.interacted_flags = {}
        self.current_eligible_interactable = None

    def add_interactable(self, interactable_obj):
        """Adds an interactable object to the manager."""
        if not hasattr(interactable_obj, 'id') or not hasattr(interactable_obj, 'get_interaction_properties'):
            print(f"Error: Object {interactable_obj} does not have required 'id' or 'get_interaction_properties' attributes.")
            return
        self.interactables.append(interactable_obj)
        self.interacted_flags[interactable_obj.id] = False # Initialize as not interacted

    def remove_interactable(self, interactable_id):
        """Removes an interactable object from the manager by its ID."""
        self.interactables = [obj for obj in self.interactables if obj.id != interactable_id]
        if interactable_id in self.interacted_flags:
            del self.interacted_flags[interactable_id]
        if self.current_eligible_interactable and self.current_eligible_interactable.id == interactable_id:
            self.current_eligible_interactable = None
            print(f"Removed active interactable: {interactable_id}")

    def update(self, player_rect_center):
        """
        Updates the state of interactions based on player position.
        Determines which interactable (if any) is currently eligible for a popup.
        Resets interaction flags if player moves sufficiently far away after an interaction.
        """
        self.current_eligible_interactable = None
        player_pos = pygame.math.Vector2(player_rect_center)

        for interactable in self.interactables:
            props = interactable.get_interaction_properties()
            # props should contain {'id': str, 'center': tuple, 'radius': int, 'message': str}
            
            interaction_center = pygame.math.Vector2(props['center'])
            distance = player_pos.distance_to(interaction_center)

            if distance < props['radius']:
                if not self.interacted_flags.get(props['id'], False):
                    self.current_eligible_interactable = interactable
                    break # Found an eligible interactable, process one at a time
            elif distance >= props['radius'] + RESET_BUFFER:
                if self.interacted_flags.get(props['id'], False):
                    self.interacted_flags[props['id']] = False
                    # print(f"Interaction for {props['id']} has been reset.")

    def get_eligible_interactable(self):
        """Returns the interactable object that is currently eligible for interaction popup."""
        return self.current_eligible_interactable

    def get_interacted_flag(self, interactable_id):
        """Checks if the player has interacted with a specific object in the current 'visit'."""
        return self.interacted_flags.get(interactable_id, True) # Default to True (already interacted) if ID is unknown

    def set_interacted_flag(self, interactable_id, status: bool):
        """Sets the interaction flag for a specific object."""
        if interactable_id in self.interacted_flags:
            self.interacted_flags[interactable_id] = status
        else:
            print(f"Warning: Tried to set interacted flag for unknown ID: {interactable_id}")

    def get_all_interactables(self):
        """Returns all registered interactable objects."""
        return self.interactables
