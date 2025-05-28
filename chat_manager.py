import pygame
import google.generativeai as genai
import os
import textwrap
from dotenv import load_dotenv

class ChatManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_active = False
        self.chat_session = None
        self.conversation_history = []
        self.current_input = ""
        self.input_active = False
        self.scroll_offset = 0
        
        # UI Configuration
        self.chat_bg_color = (20, 20, 30, 200)  # Semi-transparent dark background
        self.input_bg_color = (40, 40, 50)
        self.text_color = (255, 255, 255)
        self.player_text_color = (100, 200, 255)
        self.wizard_text_color = (255, 200, 100)
        self.border_color = (100, 100, 120)
        
        # Font setup
        pygame.font.init()
        self.font = pygame.font.Font(None, 28)
        self.input_font = pygame.font.Font(None, 32)
        
        # Layout dimensions
        self.chat_width = screen_width - 100
        self.chat_height = screen_height - 150
        self.chat_x = 50
        self.chat_y = 50
        self.input_height = 50
        self.input_y = self.chat_y + self.chat_height - self.input_height
        
        # Text wrapping width (in characters)
        self.wrap_width = 80
        
        # Initialize API
        self._init_api()
    
    def _init_api(self):
        """Initialize the Google Generative AI API"""
        try:
            load_dotenv()
            google_api_key = os.getenv("GOOGLE_API_KEY")
            
            if not google_api_key:
                print("Error: GOOGLE_API_KEY not found in .env file")
                return False
            
            genai.configure(api_key=google_api_key)
            
            model = genai.GenerativeModel(
                #model_name='gemini-1.5-flash',
                model_name='gemma-3-27b-it',
                system_instruction="You are a wise and ancient wizard with deep knowledge of magic, philosophy, and the mysteries of the universe. You are specifically interested in AI and the future. Keep your responses engaging but not too long. You are speaking to a visitor in your house who has come to seek wisdom and conversation."
            )
            
            self.chat_session = model.start_chat(history=[])
            return True
            
        except Exception as e:
            print(f"Error initializing chat API: {e}")
            return False
    
    def start_conversation(self):
        """Start a conversation with the wizard"""
        if not self.chat_session:
            print("Chat session not initialized")
            return False
        
        self.is_active = True
        self.input_active = True
        self.conversation_history = [
            ("Wizard", "Greetings, friend! Welcome to my humble abode. What brings you here today?")
        ]
        return True
    
    def end_conversation(self):
        """End the current conversation"""
        self.is_active = False
        self.input_active = False
        self.current_input = ""
        self.scroll_offset = 0
    
    def handle_event(self, event):
        """Handle pygame events for the chat interface"""
        if not self.is_active:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.end_conversation()
                return True
            elif event.key == pygame.K_RETURN:
                if self.current_input.strip():
                    self._send_message(self.current_input.strip())
                    self.current_input = ""
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.current_input = self.current_input[:-1]
                return True
            elif event.key == pygame.K_UP:
                self.scroll_offset = max(0, self.scroll_offset - 1)
                return True
            elif event.key == pygame.K_DOWN:
                max_scroll = max(0, len(self._get_wrapped_history()) - self._get_visible_lines())
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
                return True
            else:
                # Add character to input
                if len(self.current_input) < 200 and event.unicode.isprintable():
                    self.current_input += event.unicode
                return True
        
        return False
    
    def _send_message(self, message):
        """Send a message to the wizard and get response"""
        # Add player message to history
        self.conversation_history.append(("You:", message))
        
        # Send to API and get response
        try:
            response = self.chat_session.send_message(message)
            wizard_response = response.text
            self.conversation_history.append(("Wizard", wizard_response))
            
            # Auto-scroll to bottom
            self._scroll_to_bottom()
            
        except Exception as e:
            error_msg = f"The wizard seems distracted... (Error: {str(e)})"
            self.conversation_history.append(("Wizard", error_msg))
    
    def _get_wrapped_history(self):
        """Get conversation history with text wrapping applied"""
        wrapped_lines = []
        for speaker, message in self.conversation_history:
            # Wrap the message
            wrapped_message = textwrap.fill(message, width=self.wrap_width)
            lines = wrapped_message.split('\n')
            
            for i, line in enumerate(lines):
                if i == 0:
                    wrapped_lines.append(f"{speaker}: {line}")
                else:
                    wrapped_lines.append(f"{''.ljust(len(speaker) + 2)}{line}")
            wrapped_lines.append("")  # Empty line between messages
        
        return wrapped_lines
    
    def _get_visible_lines(self):
        """Calculate how many lines can fit in the chat area"""
        return (self.chat_height - self.input_height - 40) // (self.font.get_height() + 2)
    
    def _scroll_to_bottom(self):
        """Scroll to the bottom of the conversation"""
        wrapped_lines = self._get_wrapped_history()
        visible_lines = self._get_visible_lines()
        self.scroll_offset = max(0, len(wrapped_lines) - visible_lines)
    
    def draw(self, screen):
        """Draw the chat interface"""
        if not self.is_active:
            return
        
        # Create a surface for the chat with alpha
        chat_surface = pygame.Surface((self.chat_width, self.chat_height))
        chat_surface.set_alpha(230)
        chat_surface.fill(self.chat_bg_color[:3])
        
        # Draw border
        pygame.draw.rect(chat_surface, self.border_color, (0, 0, self.chat_width, self.chat_height), 3)
        
        # Draw conversation history
        self._draw_conversation(chat_surface)
        
        # Draw input area
        self._draw_input_area(chat_surface)
        
        # Draw instructions
        self._draw_instructions(chat_surface)
        
        # Blit to main screen
        screen.blit(chat_surface, (self.chat_x, self.chat_y))
    
    def _draw_conversation(self, surface):
        """Draw the conversation history"""
        wrapped_lines = self._get_wrapped_history()
        visible_lines = self._get_visible_lines()
        
        y_offset = 10
        line_height = self.font.get_height() + 2
        
        # Determine which lines to show based on scroll
        start_line = self.scroll_offset
        end_line = min(len(wrapped_lines), start_line + visible_lines)
        
        for i in range(start_line, end_line):
            line = wrapped_lines[i]
            if line.strip():  # Don't render empty lines
                # Determine color based on speaker
                if line.startswith("You:"):
                    color = self.player_text_color
                elif line.startswith("Wizard:"):
                    color = self.wizard_text_color
                else:
                    color = self.text_color
                
                text_surface = self.font.render(line, True, color)
                surface.blit(text_surface, (10, y_offset))
            
            y_offset += line_height
    
    def _draw_input_area(self, surface):
        """Draw the input area"""
        input_rect = pygame.Rect(10, self.input_y - self.chat_y, self.chat_width - 20, self.input_height)
        pygame.draw.rect(surface, self.input_bg_color, input_rect)
        pygame.draw.rect(surface, self.border_color, input_rect, 2)
        
        # Draw input text
        display_text = self.current_input
        if len(display_text) > 60:  # Limit visible characters
            display_text = "..." + display_text[-57:]
        
        # Add cursor
        cursor = "|" if pygame.time.get_ticks() % 1000 < 500 else " "
        display_text += cursor
        
        text_surface = self.input_font.render(display_text, True, self.text_color)
        surface.blit(text_surface, (input_rect.x + 5, input_rect.y + 10))
    
    def _draw_instructions(self, surface):
        """Draw instruction text"""
        instructions = [
            "Press ENTER to send message",
            "Press ESC to end conversation",
            "Use UP/DOWN arrows to scroll"
        ]
        
        y_offset = self.chat_height - 43
        for instruction in instructions:
            text_surface = pygame.font.Font(None, 20).render(instruction, True, (150, 150, 150))
            surface.blit(text_surface, (1350, y_offset))
            y_offset += 13