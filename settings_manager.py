import pygame
from databaseHandler import FirestoreHandler, SERVICE_ACCOUNT_KEY_PATH

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
        self.button_hover_color = (70, 70, 70)
        self.button_text_color = (255, 255, 255)
        self.popup_bg_color = (30, 30, 40)
        self.popup_border_color = (100, 100, 120)
        self.action_button_color = (70, 130, 180)  # Steel blue
        self.action_button_hover_color = (100, 149, 237)  # Cornflower blue
        self.close_button_color = (178, 34, 34)  # Fire brick
        self.close_button_hover_color = (220, 20, 60)  # Crimson
        self.input_field_color = (50, 50, 60)
        self.input_field_active_color = (70, 70, 80)
        self.input_field_border_color = (100, 149, 237)
        
        # Fonts
        pygame.font.init()
        self.button_font = pygame.font.Font(None, 24)
        self.popup_title_font = pygame.font.Font(None, 32)
        self.popup_button_font = pygame.font.Font(None, 26)
        self.input_font = pygame.font.Font(None, 24)
        
        # Mouse state
        self.mouse_pos = (0, 0)
        self.is_mouse_clicked = False
          # Action button rects (will be calculated in draw_popup)
        self.action_button_rects = []
        
        # Input field state
        self.show_input_fields = False
        self.input_mode = None  # "signin" or "signup"
        self.username_text = ""
        self.password_text = ""
        self.active_field = None  # "username", "password", or None
        self.username_rect = None
        self.password_rect = None
        
        # Status display properties
        self.current_username = None  # Store current signed-in username
        self.status_font = pygame.font.Font(None, 28)
        self.status_bg_color_signed_in = (40, 80, 40, 180)  # Faint green with transparency
        self.status_bg_color_signed_out = (80, 40, 40, 180)  # Faint red with transparency
        self.status_text_color = (255, 255, 255)

        # Save status box properties
        self.save_status_box_size = 45
        self.save_status_hover_font = pygame.font.Font(None, 28)

        
        # Error message display properties
        self.error_message = None
        self.error_message_start_time = 0
        self.error_display_duration = 4000  # 4 seconds in milliseconds
        self.error_font = pygame.font.Font(None, 24)
        self.error_bg_color = (80, 40, 40, 200)  # Faint red with transparency
        self.error_text_color = (255, 255, 255)
        
        # Initialize database handler
        try:
            self.db_handler = FirestoreHandler(SERVICE_ACCOUNT_KEY_PATH)
            print("Database handler initialized successfully")
        except Exception as e:
            print(f"Failed to initialize database handler: {e}")
            self.db_handler = None
    
    def update_mouse_state(self, mouse_pos, mouse_clicked):
        """Update mouse position and click state"""
        self.mouse_pos = mouse_pos
        self.is_mouse_clicked = mouse_clicked
        
    def _show_error_message(self, message):
        """Display an error message for a limited time"""
        self.error_message = message
        self.error_message_start_time = pygame.time.get_ticks()
        
    def _update_error_message(self):
        """Update error message display timer"""
        if self.error_message:
            current_time = pygame.time.get_ticks()
            if current_time - self.error_message_start_time > self.error_display_duration:
                self.error_message = None
        
    def handle_key_input(self, event):
        """Handle keyboard input for text fields"""
        if not self.show_input_fields:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Enter key pressed - validate and submit
                self._handle_input_submission()
                return True
            elif event.key == pygame.K_ESCAPE:
                # ESC now closes input fields AND the entire popup
                self._close_input_fields()
                self.is_popup_active = False  # Also close the popup
                return True
            elif event.key == pygame.K_TAB:
                # Tab key pressed - switch between fields
                if self.active_field == "username":
                    self.active_field = "password"
                elif self.active_field == "password":
                    self.active_field = "username"
                else:
                    self.active_field = "username"
                return True
            elif event.key == pygame.K_BACKSPACE:
                # Backspace - remove character
                if self.active_field == "username" and self.username_text:
                    self.username_text = self.username_text[:-1]
                elif self.active_field == "password" and self.password_text:
                    self.password_text = self.password_text[:-1]
                return True
            else:                # Regular character input
                if event.unicode.isprintable() and len(event.unicode) == 1:
                    if self.active_field == "username" and len(self.username_text) < 20:
                        self.username_text += event.unicode
                    elif self.active_field == "password" and len(self.password_text) < 20:
                        self.password_text += event.unicode
                    return True                    
        return False
    
    def _handle_input_submission(self):
        """Handle form submission when Enter is pressed"""
        if not self.username_text.strip() or not self.password_text.strip():
            self._show_error_message("Please fill in both username and password fields.")
            return
            
        if not self.db_handler:
            self._show_error_message("Database not available. Cannot authenticate.")
            return
            
        username = self.username_text.strip()
        password = self.password_text.strip()
        
        if self.input_mode == "signup":
            # Get current points from main to preserve them during signup
            current_points = self._get_current_game_points()
            success = self.db_handler.signup_user(username, password, current_points)
            if success:
                print(f"Successfully signed up user: {username}")
                self.is_signed_in = True
                self.current_username = username
                # Set saved points to current points for new account
                self._saved_points = current_points
                self._close_input_fields()
            else:
                self._show_error_message("Sign up failed. Username may already exist.")
                
        elif self.input_mode == "signin":
            success = self.db_handler.login_user(username, password)
            if success:
                print(f"Successfully signed in user: {username}")
                self.is_signed_in = True
                self.current_username = username
                # Load user's saved points
                self._load_user_points()
                self._close_input_fields()
            else:
                self._show_error_message("Sign in failed. Check your username and password.")

    def _get_current_game_points(self):
        """Get current points from the game. This should be overridden or set by main."""
        return getattr(self, '_current_points', 0)

    def set_current_points(self, points):
        """Set the current points value for signup purposes."""
        self._current_points = points

    def _load_user_points(self):
        """Load user's points from database and update the game."""
        if self.current_username and self.db_handler:
            points = self.db_handler.get_user_points(self.current_username)
            if hasattr(self, '_points_callback'):
                self._points_callback(points)
                # Set saved points to loaded value
                self._saved_points = points
                print(f"Loaded {points} points for user {self.current_username}")
            else:
                print("Warning: Points callback not set")
        else:
            print("Cannot load points: missing username or database connection")

    def set_points_callback(self, callback):
        """Set callback function to update points in main game."""
        self._points_callback = callback

    def save_user_points(self, points):
        """Save current points to database."""
        if self.current_username and self.db_handler:
            success = self.db_handler.save_user_points(self.current_username, points)
            if success:
                # Update saved points after successful save
                self._saved_points = points
            return success
        return False
        
    def _get_saved_points(self):
        """Get the last saved points value."""
        return getattr(self, '_saved_points', 0)
    
    def _is_game_saved(self):
        """Check if the current game state matches the saved state."""
        if not self.is_signed_in:
            return True  # Consider unsigned users as "saved"
        
        current_points = self._get_current_game_points()
        saved_points = self._get_saved_points()
        return current_points == saved_points
    
    def _get_save_status_info(self):
        """Get save status information for display."""
        is_saved = self._is_game_saved()
        
        if is_saved:
            return {
                'color': (60, 150, 60, 220),  # Faint green
                'hover_text': "Game saved :)"
            }
        else:
            return {
                'color': (150, 60, 60, 220),  # Faint red
                'hover_text': "Game unsaved: press Save in settings to save your progress."
            }

    def _close_input_fields(self):
        """Close input fields and reset state"""
        self.show_input_fields = False
        self.input_mode = None
        self.username_text = ""
        self.password_text = ""
        self.active_field = None
        
    def handle_click(self, mouse_pos):
        """Handle mouse clicks on buttons"""
        if self.button_rect.collidepoint(mouse_pos):
            # Toggle popup
            self.is_popup_active = not self.is_popup_active
            self._close_input_fields()  # Close input fields when toggling popup
            return True
            
        if self.is_popup_active:
            # Check if clicked outside popup to close it
            if not self.popup_rect.collidepoint(mouse_pos):
                self.is_popup_active = False
                self._close_input_fields()
                return True
                
            # Check input field clicks if they're showing
            if self.show_input_fields:
                if self.username_rect and self.username_rect.collidepoint(mouse_pos):
                    self.active_field = "username"
                    return True
                elif self.password_rect and self.password_rect.collidepoint(mouse_pos):
                    self.active_field = "password"
                    return True
            
            # Check action button clicks
            for i, button_rect in enumerate(self.action_button_rects):
                if button_rect.collidepoint(mouse_pos):
                    self._handle_action_button_click(i)
                    return True
                    
        return False
    
    def _handle_action_button_click(self, button_index):
        """Handle clicks on action buttons in the popup"""
        if self.show_input_fields:
            # When input fields are showing, button_index 0 is the submit button            
            if button_index == 0:  # Submit button
                self._handle_input_submission()
        elif self.is_signed_in:
            if button_index == 0:  # Sign Out
                print("Sign Out clicked")
                self.is_signed_in = False  # Sign out the user
                self.current_username = None  # Clear username
                print("User signed out successfully")
            elif button_index == 1:  # Save
                print("Save clicked")
                # Save current points to database
                current_points = self._get_current_game_points()
                if self.save_user_points(current_points):
                    print(f"Successfully saved {current_points} points to database.")
                else:
                    print("Failed to save points to database.")
            # Close popup after action
            self.is_popup_active = False
        else:
            if button_index == 0:  # Sign Up
                self._show_input_fields("signup")
            elif button_index == 1:  # Sign In
                self._show_input_fields("signin")
                
    def _show_input_fields(self, mode):
        """Show input fields for signin or signup"""
        self.show_input_fields = True
        self.input_mode = mode
        self.username_text = ""
        self.password_text = ""
        self.active_field = "username"  # Start with username field active
        
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
            
        # Adjust popup size based on whether input fields are showing
        if self.show_input_fields:
            popup_height = 350
            popup_width = 350
        else:
            popup_height = 200
            popup_width = 300
            
        popup_x = (self.screen_width - popup_width) // 2
        popup_y = (self.screen_height - popup_height) // 2
        current_popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw popup background with rounded corners effect
        pygame.draw.rect(screen, self.popup_bg_color, current_popup_rect, border_radius=12)
        pygame.draw.rect(screen, self.popup_border_color, current_popup_rect, 3, border_radius=12)
        
        # Draw title
        if self.show_input_fields:
            title_text = f"Sign {'Up' if self.input_mode == 'signup' else 'In'}"
        else:
            title_text = "Settings"
        title_surface = self.popup_title_font.render(title_text, True, self.button_text_color)
        title_rect = title_surface.get_rect(centerx=current_popup_rect.centerx, y=current_popup_rect.y + 20)
        screen.blit(title_surface, title_rect)
        
        if self.show_input_fields:
            self._draw_input_fields(screen, current_popup_rect)
        else:
            self._draw_action_buttons(screen, current_popup_rect)
            
        # Draw close instruction
        close_text = "Click ESC or outside of the pop-up to close"
        close_surface = pygame.font.Font(None, 20).render(close_text, True, (150, 150, 150))
        close_rect = close_surface.get_rect(centerx=current_popup_rect.centerx, 
                                          y=current_popup_rect.bottom - 30)
        screen.blit(close_surface, close_rect)
        
    def _draw_input_fields(self, screen, popup_rect):
        """Draw input fields for username and password"""
        field_width = 250
        field_height = 35
        field_spacing = 60
        
        # Username field
        username_y = popup_rect.y + 80
        username_x = popup_rect.centerx - field_width // 2
        self.username_rect = pygame.Rect(username_x, username_y, field_width, field_height)
        
        # Password field
        password_y = username_y + field_spacing
        password_x = popup_rect.centerx - field_width // 2
        self.password_rect = pygame.Rect(password_x, password_y, field_width, field_height)
        
        # Draw username label and field
        username_label = self.input_font.render("Username:", True, self.button_text_color)
        screen.blit(username_label, (username_x, username_y - 25))
        
        username_color = self.input_field_active_color if self.active_field == "username" else self.input_field_color
        pygame.draw.rect(screen, username_color, self.username_rect, border_radius=4)
        if self.active_field == "username":
            pygame.draw.rect(screen, self.input_field_border_color, self.username_rect, 2, border_radius=4)
        else:
            pygame.draw.rect(screen, self.popup_border_color, self.username_rect, 1, border_radius=4)
            
        # Draw username text
        username_surface = self.input_font.render(self.username_text, True, self.button_text_color)
        username_text_rect = username_surface.get_rect(left=self.username_rect.left + 10, centery=self.username_rect.centery)
        screen.blit(username_surface, username_text_rect)
        
        # Draw cursor for username field
        if self.active_field == "username":
            cursor_x = username_text_rect.right + 2
            cursor_y1 = self.username_rect.centery - 10
            cursor_y2 = self.username_rect.centery + 10
            pygame.draw.line(screen, self.button_text_color, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)
        
        # Draw password label and field
        password_label = self.input_font.render("Password:", True, self.button_text_color)
        screen.blit(password_label, (password_x, password_y - 25))
        
        password_color = self.input_field_active_color if self.active_field == "password" else self.input_field_color
        pygame.draw.rect(screen, password_color, self.password_rect, border_radius=4)
        if self.active_field == "password":
            pygame.draw.rect(screen, self.input_field_border_color, self.password_rect, 2, border_radius=4)
        else:
            pygame.draw.rect(screen, self.popup_border_color, self.password_rect, 1, border_radius=4)
            
        # Draw password text (masked with asterisks)
        masked_password = "*" * len(self.password_text)
        password_surface = self.input_font.render(masked_password, True, self.button_text_color)
        password_text_rect = password_surface.get_rect(left=self.password_rect.left + 10, centery=self.password_rect.centery)
        screen.blit(password_surface, password_text_rect)
        
        # Draw cursor for password field
        if self.active_field == "password":
            cursor_x = password_text_rect.right + 2
            cursor_y1 = self.password_rect.centery - 10
            cursor_y2 = self.password_rect.centery + 10
            pygame.draw.line(screen, self.button_text_color, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)
            
        # Draw submit button
        submit_button_width = 100
        submit_button_height = 35
        submit_button_x = popup_rect.centerx - submit_button_width // 2
        submit_button_y = password_y + 80
        submit_button_rect = pygame.Rect(submit_button_x, submit_button_y, submit_button_width, submit_button_height)
        
        submit_color = self.action_button_hover_color if self._is_button_hovered(submit_button_rect) else self.action_button_color
        pygame.draw.rect(screen, submit_color, submit_button_rect, border_radius=6)
        pygame.draw.rect(screen, self.popup_border_color, submit_button_rect, 2, border_radius=6)
        
        submit_text = "Submit"
        submit_surface = self.popup_button_font.render(submit_text, True, self.button_text_color)
        submit_text_rect = submit_surface.get_rect(center=submit_button_rect.center)
        screen.blit(submit_surface, submit_text_rect)
        
        # Update action button rects to include submit button
        self.action_button_rects = [submit_button_rect]
        
        # Draw instructions
        instruction_text = "Press Enter to submit, Tab to switch fields, Esc to cancel"
        instruction_surface = pygame.font.Font(None, 18).render(instruction_text, True, (150, 150, 150))
        instruction_rect = instruction_surface.get_rect(centerx=popup_rect.centerx, y=submit_button_y + 50)
        screen.blit(instruction_surface, instruction_rect)
        
    def _draw_action_buttons(self, screen, popup_rect):
        """Draw the original action buttons (Sign In/Sign Up or Sign Out/Save)"""
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
        start_x = popup_rect.centerx - total_buttons_width // 2
        button_y = popup_rect.centery + 10
        
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
    
    def draw(self, screen):
        """Draw both the settings button and popup if active"""
        # Update error message timer
        self._update_error_message()
        
        self.draw_settings_button(screen)
        self.draw_popup(screen)
        self._draw_status_display(screen)
        self._draw_error_message(screen)
        
    def _draw_status_display(self, screen):
        """Draw the sign-in status display in the middle of the screen"""
        if self.is_signed_in and self.current_username:
            status_text = f"Signed in as: {self.current_username}"
            bg_color = self.status_bg_color_signed_in
        else:
            status_text = "Not signed in"
            bg_color = self.status_bg_color_signed_out
        
        # Render text
        text_surface = self.status_font.render(status_text, True, self.status_text_color)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        
        # Position at center-top of screen
        padding = 15
        box_width = text_width + padding * 2
        box_height = text_height + padding
        box_x = (self.screen_width - box_width) // 2
        box_y = 20  # Position near top of screen
        
        # Create a surface with alpha for transparency
        status_surface = pygame.Surface((box_width, box_height))
        status_surface.set_alpha(bg_color[3])  # Set transparency
        status_surface.fill(bg_color[:3])  # Fill with RGB color
        
        # Draw background with border
        screen.blit(status_surface, (box_x, box_y))
        pygame.draw.rect(screen, self.popup_border_color, (box_x, box_y, box_width, box_height), 2, border_radius=8)
        
        # Draw text
        text_x = box_x + padding
        text_y = box_y + padding // 2
        screen.blit(text_surface, (text_x, text_y))

        # Draw save status box to the right of the status display
        self._draw_save_status_box(screen, box_x + box_width + 10, box_y + (box_height - self.save_status_box_size) // 2)

    def _draw_save_status_box(self, screen, x, y):
        """Draw the save status indicator box."""
        if not self.is_signed_in:
            return  # Don't show save status if not signed in
            
        save_info = self._get_save_status_info()
        box_rect = pygame.Rect(x, y, self.save_status_box_size, self.save_status_box_size)
        
        # Create surface with alpha for the colored background
        box_surface = pygame.Surface((self.save_status_box_size, self.save_status_box_size))
        box_surface.set_alpha(save_info['color'][3])
        box_surface.fill(save_info['color'][:3])
        
        # Draw the box
        screen.blit(box_surface, (x, y))
        pygame.draw.rect(screen, self.popup_border_color, box_rect, 2, border_radius=4)
        
        # Check if mouse is hovering over the box
        if box_rect.collidepoint(self.mouse_pos):
            self._draw_save_status_tooltip(screen, save_info['hover_text'], x, y)

    def _draw_save_status_tooltip(self, screen, text, box_x, box_y):
        """Draw tooltip for save status box on hover."""
        # Render tooltip text
        tooltip_surface = self.save_status_hover_font.render(text, True, self.status_text_color)
        tooltip_width = tooltip_surface.get_width()
        tooltip_height = tooltip_surface.get_height()
        
        # Position tooltip above the box
        tooltip_padding = 8
        tooltip_box_width = tooltip_width + tooltip_padding * 2
        tooltip_box_height = tooltip_height + tooltip_padding
        
        # Calculate tooltip position (above the save status box)
        tooltip_x = box_x - (tooltip_box_width - self.save_status_box_size) // 2
        tooltip_y = box_y - tooltip_box_height - 8
        
        # Ensure tooltip stays on screen
        tooltip_x = max(5, min(tooltip_x, self.screen_width - tooltip_box_width - 5))
        tooltip_y = max(5, tooltip_y)
        
        # Create tooltip background
        tooltip_bg_surface = pygame.Surface((tooltip_box_width, tooltip_box_height))
        tooltip_bg_surface.set_alpha(200)
        tooltip_bg_surface.fill((40, 40, 50))
        
        # Draw tooltip
        screen.blit(tooltip_bg_surface, (tooltip_x, tooltip_y))
        pygame.draw.rect(screen, self.popup_border_color, 
                        (tooltip_x, tooltip_y, tooltip_box_width, tooltip_box_height), 
                        1, border_radius=4)
        
        # Draw tooltip text
        text_x = tooltip_x + tooltip_padding
        text_y = tooltip_y + tooltip_padding // 2
        screen.blit(tooltip_surface, (text_x, text_y))

    def _draw_error_message(self, screen):
        """Draw error message below the settings popup if there is one"""
        if not self.error_message:
            return
            
        # Render error text
        error_text_surface = self.error_font.render(self.error_message, True, self.error_text_color)
        text_width = error_text_surface.get_width()
        text_height = error_text_surface.get_height()
        
        # Position below popup area
        padding = 12
        box_width = text_width + padding * 2
        box_height = text_height + padding
        box_x = (self.screen_width - box_width) // 2
        box_y = (self.screen_height // 2) + 200  # Below popup area
        
        # Create a surface with alpha for transparency
        error_surface = pygame.Surface((box_width, box_height))
        error_surface.set_alpha(self.error_bg_color[3])  # Set transparency
        error_surface.fill(self.error_bg_color[:3])  # Fill with RGB color
        
        # Draw background with border
        screen.blit(error_surface, (box_x, box_y))
        pygame.draw.rect(screen, self.popup_border_color, (box_x, box_y, box_width, box_height), 2, border_radius=6)
        
        # Draw error text
        text_x = box_x + padding
        text_y = box_y + padding // 2
        screen.blit(error_text_surface, (text_x, text_y))
        
    def set_signed_in_state(self, is_signed_in):
        """Update the player's sign-in state"""
        self.is_signed_in = is_signed_in
