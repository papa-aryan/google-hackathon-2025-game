import pygame
from databaseHandler import DatabaseHandler

class QuoteTracker:
    def __init__(self):
        """Initialize the quote tracker"""
        self.db_handler = None
        try:
            self.db_handler = DatabaseHandler()
        except Exception as e:
            print(f"QuoteTracker: Failed to initialize database handler: {e}")
        
        # Total available quotes (matching naval_npc.py)
        self.total_quote_ids = list(range(1, 6))  # [1, 2, 3, 4, 5]
        
        # UI state
        self.is_popup_active = False
        self.current_username = None

        # Cache for quote data to prevent repeated database calls
        self._cached_quote_data = {}
        self._cached_username = None
        
        # UI configuration (following QuizManager pattern)
        pygame.font.init()
        self.screen_width = 1700  # Will be set properly when popup is shown
        self.screen_height = 900
        
        # Colors (matching QuizManager style)
        self.popup_bg_color = (25, 35, 50)  # Dark blue
        self.border_color = (100, 150, 200)  # Light blue border
        self.text_color = (255, 255, 255)  # White text
        self.unlocked_bg_color = (40, 80, 40)  # Dark green for unlocked
        self.locked_bg_color = (60, 60, 60)  # Dark gray for locked
        self.quote_border_color = (150, 150, 150)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.quote_font = pygame.font.Font(None, 30)
        self.number_font = pygame.font.Font(None, 32)
        self.progress_font = pygame.font.Font(None, 36)
        
        # Layout
        self.popup_width = 900
        self.popup_height = 650

        # REMOVE THESE TWO?
        #self.last_popup_time = 0
        #self.popup_cooldown_ms = 4000  # 4 second cooldown
        
        self.last_close_time = 0
        self.reopen_cooldown_ms = 1000  # 1 second cooldown after closing

    def show_quote_tracker_popup(self, username):
        """Show quote tracker popup UI"""
        current_time = pygame.time.get_ticks()
        
        # Check cooldown to prevent spam re-opening
        if current_time - self.last_close_time < self.reopen_cooldown_ms:
            return  # Still in cooldown, ignore activation
            
        self.current_username = username
        self.is_popup_active = True
        
        # Reset cache when popup opens to ensure fresh data
        if hasattr(self, '_cached_quote_status'):
            delattr(self, '_cached_quote_status')
        # Cache quote data when popup opens to prevent repeated DB calls
        self._cache_quote_data_for_user(username)

    def _cache_quote_data_for_user(self, username):
        """Cache quote data to prevent repeated database calls during drawing"""
        if not self.db_handler or username == self._cached_username:
            return  # Already cached for this user
            
        self._cached_quote_data = {}
        self._cached_username = username
        
        if username:  # Only cache if user is signed in
            try:
                # Pre-fetch all quote content
                for quote_id in self.total_quote_ids:
                    quote_data = self.db_handler.read_document("naval_quotes", str(quote_id))
                    if quote_data and "quote" in quote_data:
                        self._cached_quote_data[quote_id] = quote_data["quote"]
            except Exception as e:
                print(f"Error caching quote data: {e}")
    
    def handle_event(self, event):
        """Handle pygame events for the quote tracker popup"""
        if not self.is_popup_active:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Close popup and start cooldown
                self.is_popup_active = False
                self.last_close_time = pygame.time.get_ticks()  # Start cooldown on close
                return True  # Only consume ESC key events
                
        # Don't consume other events - let them pass through to main game loop
        return False
    
    def should_disable_main_game_elements(self):
        """Returns True if main game elements should be disabled during popup"""
        return self.is_popup_active
    
    def draw(self, screen):
        """Draw the quote tracker popup"""
        if not self.is_popup_active:
            return
            
        # Update screen dimensions
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Create overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Calculate popup position
        popup_x = (self.screen_width - self.popup_width) // 2
        popup_y = (self.screen_height - self.popup_height) // 2
        
        # Draw main popup
        popup_surface = pygame.Surface((self.popup_width, self.popup_height))
        popup_surface.fill(self.popup_bg_color)
        
        # Draw border
        pygame.draw.rect(popup_surface, self.border_color, 
                        (0, 0, self.popup_width, self.popup_height), 4)
        
        if self.current_username:
            self._draw_quote_tracker_content(popup_surface)
        else:
            self._draw_sign_in_message(popup_surface)
            
        screen.blit(popup_surface, (popup_x, popup_y))
    
    def _draw_sign_in_message(self, surface):
        """Draw sign in message for non-signed-in users"""
        y_offset = 50
        
        # Title
        title_text = self.title_font.render("🏆 Quote Tracker", True, self.text_color)
        title_x = (self.popup_width - title_text.get_width()) // 2
        surface.blit(title_text, (title_x, y_offset))
        y_offset += title_text.get_height() + 50
        
        # Sign in message
        sign_in_text = self.progress_font.render("Sign in to track your progress", True, (200, 200, 200))
        sign_in_x = (self.popup_width - sign_in_text.get_width()) // 2
        surface.blit(sign_in_text, (sign_in_x, y_offset))
        y_offset += sign_in_text.get_height() + 30
        
        # Instructions
        instruction_text = self.quote_font.render("Unlock quotes by talking to the Naval Officer", True, (150, 150, 150))
        instruction_x = (self.popup_width - instruction_text.get_width()) // 2
        surface.blit(instruction_text, (instruction_x, y_offset))
        y_offset += instruction_text.get_height() + 50
        
        # Close instruction
        close_text = self.quote_font.render("Press ESC to close", True, (150, 150, 150))
        close_x = (self.popup_width - close_text.get_width()) // 2
        surface.blit(close_text, (close_x, self.popup_height - 40))
    
    def _draw_quote_tracker_content(self, surface):
        """Draw the full quote tracker content for signed-in users"""
        if not self.db_handler:
            return
        
        try:
            # Use cached status instead of calling get_quote_status repeatedly
            if not hasattr(self, '_cached_quote_status') or self._cached_username != self.current_username:
                self._cache_quote_status()
            
            quote_status = self._cached_quote_status
            unlocked_quotes = quote_status["unlocked"]
            locked_quotes = quote_status["locked"]
            
            y_offset = 20
            
            # Title
            title_text = self.title_font.render("🏆 Quote Tracker", True, self.text_color)
            title_x = (self.popup_width - title_text.get_width()) // 2
            surface.blit(title_text, (title_x, y_offset))
            y_offset += title_text.get_height() + 10
            
            # Progress
            progress_text = self.progress_font.render(quote_status["progress"] + " quotes unlocked", True, (100, 255, 100))
            progress_x = (self.popup_width - progress_text.get_width()) // 2
            surface.blit(progress_text, (progress_x, y_offset))
            y_offset += progress_text.get_height() + 30
            
            # Draw quotes (unlocked first, then locked)
            quote_box_width = self.popup_width - 40
            quote_box_height = 70

            # Draw unlocked quotes first
            for quote_id in unlocked_quotes:
                y_offset = self._draw_quote_box(surface, quote_id, True, 20, y_offset, quote_box_width, quote_box_height)
                y_offset += 10  # Spacing between boxes
            
            # Draw locked quotes
            for quote_id in locked_quotes:
                y_offset = self._draw_quote_box(surface, quote_id, False, 20, y_offset, quote_box_width, quote_box_height)
                y_offset += 10  # Spacing between boxes
            
            # Close instruction
            close_text = self.quote_font.render("Press ESC to close", True, (150, 150, 150))
            close_x = (self.popup_width - close_text.get_width()) // 2
            surface.blit(close_text, (close_x, self.popup_height - 30))
            
        except Exception as e:
            print(f"Error drawing quote tracker content: {e}")

    def _cache_quote_status(self):
        """Cache quote status to prevent repeated database calls"""
        if not self.db_handler or not self.current_username:
            self._cached_quote_status = {"unlocked": [], "locked": self.total_quote_ids, "progress": f"0/{len(self.total_quote_ids)}"}
            return
            
        try:
            unlocked_quotes = self.db_handler.get_user_unlocked_quotes(self.current_username)
            locked_quotes = [qid for qid in self.total_quote_ids if qid not in unlocked_quotes]
            
            self._cached_quote_status = {
                "unlocked": sorted(unlocked_quotes),
                "locked": sorted(locked_quotes),
                "progress": f"{len(unlocked_quotes)}/{len(self.total_quote_ids)}"
            }
        except Exception as e:
            print(f"QuoteTracker _cache_quote_status error: {e}")
            self._cached_quote_status = {"unlocked": [], "locked": self.total_quote_ids, "progress": f"0/{len(self.total_quote_ids)}"}

    
    def _draw_quote_box(self, surface, quote_id, is_unlocked, x, y, width, height):
        """Draw a single quote box and return the new y position"""
        # Choose colors based on unlock status
        bg_color = self.unlocked_bg_color if is_unlocked else self.locked_bg_color
        
        # Draw quote box background
        quote_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, bg_color, quote_rect)
        pygame.draw.rect(surface, self.quote_border_color, quote_rect, 2)
        
        # Draw quote number
        number_text = self.number_font.render(f"#{quote_id}", True, self.text_color)
        surface.blit(number_text, (x + 10, y + 10))
        
        # Draw quote content
        if is_unlocked:
            # Use cached quote data instead of database call
            if quote_id in self._cached_quote_data:
                quote_text = self._cached_quote_data[quote_id]
                # Wrap text to fit in box
                wrapped_lines = self._wrap_text(quote_text, self.quote_font, width - 80)
                
                text_y = y + 15
                for line in wrapped_lines[:2]:  # Show max 2 lines
                    line_surface = self.quote_font.render(line, True, self.text_color)
                    surface.blit(line_surface, (x + 60, text_y))
                    text_y += self.quote_font.get_height() + 2
                    
                # Add "..." if text was truncated
                if len(wrapped_lines) > 2:
                    ellipsis = self.quote_font.render("...", True, (200, 200, 200))
                    surface.blit(ellipsis, (x + 60, text_y))
            else:
                error_text = self.quote_font.render("Quote not found", True, (255, 100, 100))
                surface.blit(error_text, (x + 60, y + 25))
        else:
            # Show question marks for locked quotes
            locked_text = self.quote_font.render("??? ??? ??? ???", True, (120, 120, 120))
            surface.blit(locked_text, (x + 60, y + 25))
        
        return y + height

    
    def _wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    lines.append(word)  # Word too long, add anyway
        
        if current_line:
            lines.append(current_line)
        
        return lines

    # Keep existing methods for backward compatibility
    def print_quote_status(self, username):
        """Print locked and unlocked quotes to console for MVP"""
        # Disabled to prevent spam - UI popup is now the primary interface
        pass
        if not self.db_handler or not username:
            print("QuoteTracker: Cannot check quotes - no database or username")
            return
            
        try:
            # Get user's unlocked quotes
            unlocked_quotes = self.db_handler.get_user_unlocked_quotes(username)
            locked_quotes = [qid for qid in self.total_quote_ids if qid not in unlocked_quotes]
            
            print("\n" + "="*50)
            print("QUOTE TRACKER - MVP CONSOLE OUTPUT")
            print("="*50)
            print(f"User: {username}")
            print(f"Progress: {len(unlocked_quotes)}/{len(self.total_quote_ids)} quotes unlocked")
            print("-"*50)
            
            # Print unlocked quotes with content
            print("UNLOCKED QUOTES:")
            if unlocked_quotes:
                for quote_id in sorted(unlocked_quotes):
                    quote_data = self.db_handler.read_document("naval_quotes", str(quote_id))
                    if quote_data and "quote" in quote_data:
                        print(f"  [{quote_id}] {quote_data['quote']}")
                    else:
                        print(f"  [{quote_id}] (Quote not found in database)")
            else:
                print("  None unlocked yet")
                
            print("\nLOCKED QUOTES:")
            if locked_quotes:
                for quote_id in sorted(locked_quotes):
                    print(f"  [{quote_id}] ???")
            else:
                print("  All quotes unlocked!")
                
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"QuoteTracker error: {e}")
    
    def get_quote_status(self, username):
        """Get quote status data for UI purposes (for later steps)"""
        if not self.db_handler or not username:
            return {"unlocked": [], "locked": self.total_quote_ids}
            
        try:
            unlocked_quotes = self.db_handler.get_user_unlocked_quotes(username)
            locked_quotes = [qid for qid in self.total_quote_ids if qid not in unlocked_quotes]
            
            return {
                "unlocked": sorted(unlocked_quotes),
                "locked": sorted(locked_quotes),
                "progress": f"{len(unlocked_quotes)}/{len(self.total_quote_ids)}"
            }
        except Exception as e:
            print(f"QuoteTracker get_quote_status error: {e}")
            return {"unlocked": [], "locked": self.total_quote_ids}