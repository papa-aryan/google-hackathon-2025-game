import pygame

class SettingsManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_popup_active = False
        self.is_signed_in = False  # Player state - will be implemented later
        
        # Button dimensions and positioning
        self.button_width = 80
        self.button_height = 40
        self.button_x = screen_width - self.button_width - 20  # 20px from right edge
        self.button_y = 20  # 20px from top
        self.button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        
        # Popup dimensions
        self.popup_width = 300
        self.popup_height = 200
        self.popup_x = (screen_width - self.popup_width) // 2
        self.popup_y = (screen_height - self.popup_height) // 2
        self.popup_rect = pygame.Rect(self.popup_x, self.popup_y, self.popup_width, self.popup_height)
        
        # Colors - modern theme
        self.button_color = (40, 40, 50)
        self.button_hover_color = (60, 60, 70)
        self.button_text_color = (255, 255, 255)
        self.popup_bg_color = (30, 30, 40)
        self.popup_border_color = (100, 100, 120)
        self.action_button_color = (70, 130, 180)  # Steel blue
        self.action_button_hover_color = (100, 149, 237)  # Cornflower blue
        self.close_button_color = (178, 34, 34)  # Fire brick
        self.close_button_hover_color = (220, 20, 60)  # Crimson
        
        # Fonts
        pygame.font.init()
        self.button_font = pygame.font.Font(None, 24)
        self.popup_title_font = pygame.font.Font(None, 32)
        self.popup_button_font = pygame.font.Font(None, 26)
        
        # Mouse state
        self.mouse_pos = (0, 0)
        self.is_mouse_clicked = False
        
        # Action button rects (will be calculated in draw_popup)
        self.action_button_rects = []
        
    def update_mouse_state(self, mouse_pos, mouse_clicked):
        """Update mouse position and click state"""
        self.mouse_pos = mouse_pos
        self.is_mouse_clicked = mouse_clicked
        
    def handle_click(self, mouse_pos):
        """Handle mouse clicks on buttons"""
        if self.button_rect.collidepoint(mouse_pos):
            # Toggle popup
            self.is_popup_active = not self.is_popup_active
            return True
            
        if self.is_popup_active:
            # Check if clicked outside popup to close it
            if not self.popup_rect.collidepoint(mouse_pos):
                self.is_popup_active = False
                return True
                
            # Check action button clicks
            for i, button_rect in enumerate(self.action_button_rects):
                if button_rect.collidepoint(mouse_pos):
                    self._handle_action_button_click(i)
                    return True
                    
        return False
        
    def _handle_action_button_click(self, button_index):
        """Handle clicks on action buttons in the popup"""
        if self.is_signed_in:
            if button_index == 0:  # Sign Out
                print("Sign Out clicked")
                # TODO: Implement sign out logic
            elif button_index == 1:  # Save
                print("Save clicked") 
                # TODO: Implement save logic
        else:
            if button_index == 0:  # Sign Up
                print("Sign Up clicked")
                # TODO: Implement sign up logic
            elif button_index == 1:  # Sign In
                print("Sign In clicked")
                # TODO: Implement sign in logic
                
        # Close popup after action
        self.is_popup_active = False
        
    def _is_button_hovered(self, button_rect):
        """Check if a button is being hovered"""
        return button_rect.collidepoint(self.mouse_pos)
        
    def draw_settings_button(self, screen):
        """Draw the settings button in the top right corner"""
        # Choose color based on hover state
        button_color = self.button_hover_color if self._is_button_hovered(self.button_rect) else self.button_color
        
        # Draw button with rounded corners effect (multiple rects with decreasing size)
        pygame.draw.rect(screen, button_color, self.button_rect, border_radius=8)
        pygame.draw.rect(screen, self.popup_border_color, self.button_rect, 2, border_radius=8)
        
        # Draw button text
        button_text = self.button_font.render("Settings", True, self.button_text_color)
        text_rect = button_text.get_rect(center=self.button_rect.center)
        screen.blit(button_text, text_rect)
        
    def draw_popup(self, screen):
        """Draw the settings popup if active"""
        if not self.is_popup_active:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw popup background with rounded corners effect
        pygame.draw.rect(screen, self.popup_bg_color, self.popup_rect, border_radius=12)
        pygame.draw.rect(screen, self.popup_border_color, self.popup_rect, 3, border_radius=12)
        
        # Draw title
        title_text = "Settings"
        title_surface = self.popup_title_font.render(title_text, True, self.button_text_color)
        title_rect = title_surface.get_rect(centerx=self.popup_rect.centerx, y=self.popup_rect.y + 20)
        screen.blit(title_surface, title_rect)
        
        # Draw action buttons based on sign-in state
        self.action_button_rects = []  # Reset button rects
        button_width = 120
        button_height = 40
        button_spacing = 20
        
        if self.is_signed_in:
            button_texts = ["Sign Out", "Save"]
            button_colors = [self.close_button_color, self.action_button_color]
            button_hover_colors = [self.close_button_hover_color, self.action_button_hover_color]
        else:
            button_texts = ["Sign Up", "Sign In"]
            button_colors = [self.action_button_color, self.action_button_color]
            button_hover_colors = [self.action_button_hover_color, self.action_button_hover_color]
        
        # Calculate button positions
        total_buttons_width = len(button_texts) * button_width + (len(button_texts) - 1) * button_spacing
        start_x = self.popup_rect.centerx - total_buttons_width // 2
        button_y = self.popup_rect.centery + 10
        
        for i, (text, color, hover_color) in enumerate(zip(button_texts, button_colors, button_hover_colors)):
            button_x = start_x + i * (button_width + button_spacing)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.action_button_rects.append(button_rect)
            
            # Choose color based on hover state
            current_color = hover_color if self._is_button_hovered(button_rect) else color
            
            # Draw button
            pygame.draw.rect(screen, current_color, button_rect, border_radius=6)
            pygame.draw.rect(screen, self.popup_border_color, button_rect, 2, border_radius=6)
            
            # Draw button text
            button_text_surface = self.popup_button_font.render(text, True, self.button_text_color)
            text_rect = button_text_surface.get_rect(center=button_rect.center)
            screen.blit(button_text_surface, text_rect)
            
        # Draw close instruction
        close_text = "Click outside to close"
        close_surface = pygame.font.Font(None, 20).render(close_text, True, (150, 150, 150))
        close_rect = close_surface.get_rect(centerx=self.popup_rect.centerx, 
                                          y=self.popup_rect.bottom - 30)
        screen.blit(close_surface, close_rect)
        
    def draw(self, screen):
        """Draw both the settings button and popup if active"""
        self.draw_settings_button(screen)
        self.draw_popup(screen)
        
    def set_signed_in_state(self, is_signed_in):
        """Update the player's sign-in state"""
        self.is_signed_in = is_signed_in
