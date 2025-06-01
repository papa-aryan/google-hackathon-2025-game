import pygame
import random
import google.generativeai as genai
import os
from dotenv import load_dotenv
from databaseHandler import DatabaseHandler

class QuizManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_active = False
        self.current_question = None
        self.player_answer = ""
        self.evaluating = False
        self.quiz_result = None
        self.pending_collectible_points = 0
        self.show_result_popup = False
        self.attempt_count = 0
        self.max_attempts = 3
          # Initialize database handler
        try:
            self.db_handler = DatabaseHandler()
        except Exception as e:
            print(f"Failed to initialize database handler: {e}")
            self.db_handler = None
        
        # Initialize continuous API chat
        self.chat_session = None
        self._init_api()
        
        # UI Configuration
        self.popup_bg_color = (30, 30, 40)
        self.border_color = (100, 150, 200)
        self.text_color = (255, 255, 255)
        self.input_bg_color = (50, 50, 60)
        self.input_border_color = (120, 180, 220)
        self.button_color = (70, 120, 170)
        self.button_hover_color = (90, 140, 190)
        
        # Font setup
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 48)
        self.question_font = pygame.font.Font(None, 32)
        self.input_font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font(None, 36)
        
        # Layout
        self.popup_width = min(800, screen_width - 100)
        self.popup_height = min(600, screen_height - 100)
        self.popup_x = (screen_width - self.popup_width) // 2
        self.popup_y = (screen_height - self.popup_height) // 2
        
        # Callbacks
        self.completion_callback = None
        self.failure_callback = None
    
    def _init_api(self):
        """Initialize the Google Generative AI API for continuous chat"""
        try:
            load_dotenv()
            google_api_key = os.getenv("GOOGLE_API_KEY")
            
            if not google_api_key:
                print("Error: GOOGLE_API_KEY not found in .env file")
                return False
            
            genai.configure(api_key=google_api_key)
            
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction="You are an AI teacher evaluating student answers. You should be helpful but fair in your evaluation. Keep responses concise and educational."
            )
            
            self.chat_session = model.start_chat(history=[])
            return True
            
        except Exception as e:
            print(f"Error initializing quiz API: {e}")
            return False
    
    def start_quiz(self, collectible_points=1):
        """Start a new quiz with a random question"""
        if not self.db_handler or not self.chat_session:
            print("Quiz system not properly initialized")
            return False
        
        # Fetch random question from database
        question_data = self._fetch_random_question()
        if not question_data:
            print("Failed to fetch question from database")
            return False
        
        self.is_active = True
        self.current_question = question_data
        self.player_answer = ""
        self.evaluating = False
        self.quiz_result = None
        self.show_result_popup = False
        self.pending_collectible_points = collectible_points
        self.attempt_count = 0
        
        print(f"Quiz started! Question: {question_data.get('question_text', 'No question text')}")
        return True
    
    def _fetch_random_question(self):
        """Fetch a random question from the ai_questions collection"""
        try:
            # Get a random question ID (1-30)
            #question_id = str(random.randint(1, 30))
            #question_id = "1"
            question_id = str(random.randint(1, 2))
            

            # Read the question document
            question_doc = self.db_handler.read_document('ai_questions', question_id)
            if question_doc:
                print(f"Fetched question ID {question_id}: {question_doc.get('question_text', 'No text')}")
                return question_doc
            else:
                print(f"No question found with ID {question_id}")
                return None
        except Exception as e:
            print(f"Error fetching random question: {e}")
            return None
    
    def handle_event(self, event):
        """Handle pygame events for the quiz interface"""
        if not self.is_active:
            return False
        
        # Handle result popup events (Enter to continue like timeout)
        if self.show_result_popup:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Do EXACTLY what the timeout does
                    self.show_result_popup = False
                    
                    # Close quiz if it was completed or failed
                    if (self.quiz_result and
                        ("Correct!" in self.quiz_result or 
                        "Maximum attempts reached" in self.quiz_result)):
                        success = self.quiz_result and "Correct!" in self.quiz_result
                        self._close_quiz(bool(success))
                    else:
                        # Clear answer for next attempt (retry)
                        self.player_answer = ""
                    return True
                elif event.key == pygame.K_ESCAPE:
                    # Escape always closes quiz
                    self._close_quiz(False)
                    return True
            return True  # Consume all events during result popup
            
        if self.evaluating:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._close_quiz(False)  # Close without success
                return True
            elif event.key == pygame.K_RETURN:
                if self.player_answer.strip():
                    self._submit_answer()
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.player_answer = self.player_answer[:-1]
                return True
            else:
                # Add character to input
                if len(self.player_answer) < 450 and event.unicode.isprintable():
                    self.player_answer += event.unicode
                return True
        
        return False
    
    def _submit_answer(self):
        """Submit the player's answer for evaluation"""
        if not self.current_question or not self.player_answer.strip():
            print("DEBUG: No question or empty answer, returning")
            return
        
        print(f"DEBUG: Submitting answer: '{self.player_answer}'")
        self.evaluating = True
        self.attempt_count += 1
        
        # Create evaluation prompt
        prompt = f"""Evaluate if the player's answer is correct for the given question. Use the expected keywords, as well as your knowledge as an AI, to evaluate the answer.
Question: '{self.current_question.get('question_text', '')}'
Expected Concepts: '{self.current_question.get('answer_keywords', '')}'
Player's Answer: '{self.player_answer}'
Please respond with 'CORRECT' if the answer is sufficiently accurate, otherwise 'INCORRECT'. You can consider synonyms and related concepts. If 'CORRECT', optionally follow up a brief reason why. If 'INCORRECT', follow up with clear hints towards the correct answer, but do not reveal the full answer."""
        
        print(f"DEBUG: Sending prompt to AI: {prompt[:200]}...")
    
        try:
            # Send to continuous chat session
            response = self.chat_session.send_message(prompt)
            ai_response = response.text
    
            print(f"DEBUG: AI Response received: '{ai_response}'")

            # Process the AI response
            self._process_ai_response(ai_response)
            
        except Exception as e:
            print(f"DEBUG: Error in _submit_answer: {e}")
            self.evaluating = False
            # Show error message to player
            self.quiz_result = "Error occurred during evaluation. Please try again."
            self._show_result_popup()
    
    def _process_ai_response(self, ai_response):
        """Process the AI's evaluation response"""
        print(f"DEBUG: Processing AI response: '{ai_response}'")
        self.evaluating = False
        
        # More precise checking - look for the exact words at the start
        response_upper = ai_response.upper().strip()
        
        # Check if answer was correct (look for CORRECT at the beginning)
        if response_upper.startswith("CORRECT"):
            print("DEBUG: AI response starts with 'CORRECT' - awarding points")
            # Award points and close quiz
            self.quiz_result = f"Correct! +{self.pending_collectible_points} point(s)\n\n{ai_response}"
            self._show_result_popup()
            if self.completion_callback:
                print("DEBUG: Calling completion callback")
                self.completion_callback(self.pending_collectible_points)
        else:
            print("DEBUG: AI response does NOT start with 'CORRECT' - marked as incorrect")
            # Answer was incorrect
            if self.attempt_count >= self.max_attempts:
                # Max attempts reached, no points awarded
                self.quiz_result = f"Maximum attempts reached. No points awarded.\n\n{ai_response}"
                self._show_result_popup()
                if self.failure_callback:
                    print("DEBUG: Calling failure callback")
                    self.failure_callback()
            else:
                # Give feedback and allow retry
                attempts_left = self.max_attempts - self.attempt_count
                self.quiz_result = f"Incorrect. {attempts_left} attempt(s) remaining.\n\n{ai_response}\n\nTry again!"
                self._show_result_popup()
                # Don't close quiz, allow player to try again
    
    def _show_result_popup(self):
        """Show the result popup with AI feedback"""
        self.show_result_popup = True
    
    def update(self):
        """Update quiz state"""
        if not self.is_active:
            return        # Handle result popup timeout
    
    def _close_quiz(self, success=False):
        """Close the quiz"""
        self.is_active = False
        self.current_question = None
        self.player_answer = ""
        self.evaluating = False
        self.quiz_result = None
        self.show_result_popup = False
        self.attempt_count = 0
        print(f"Quiz closed. Success: {success}")
    
    def draw(self, screen):
        """Draw the quiz interface"""
        if not self.is_active:
            return
        
        # Create overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw main popup
        popup_surface = pygame.Surface((self.popup_width, self.popup_height))
        popup_surface.fill(self.popup_bg_color)
        
        # Draw border
        pygame.draw.rect(popup_surface, self.border_color, 
                        (0, 0, self.popup_width, self.popup_height), 4)
        
        if self.show_result_popup:
            self._draw_result_popup(popup_surface)
        elif self.evaluating:
            self._draw_evaluating_screen(popup_surface)
        else:
            self._draw_question_screen(popup_surface)
        
        screen.blit(popup_surface, (self.popup_x, self.popup_y))
    
    def _draw_question_screen(self, surface):
        """Draw the main question interface"""
        y_offset = 20
        
        # Title
        title_text = self.title_font.render("AI Knowledge Quiz", True, self.text_color)
        title_x = (self.popup_width - title_text.get_width()) // 2
        surface.blit(title_text, (title_x, y_offset))
        y_offset += title_text.get_height() + 30
        
        # Question text with wrapping
        if self.current_question:
            question_text = self.current_question.get('question_text', 'No question available')
            wrapped_lines = self._wrap_text(question_text, self.question_font, self.popup_width - 40)
            
            for line in wrapped_lines:
                line_surface = self.question_font.render(line, True, self.text_color)
                surface.blit(line_surface, (20, y_offset))
                y_offset += line_surface.get_height() + 5
        
        y_offset += 20
        
        # Input field
        input_label = self.question_font.render("Your Answer:", True, self.text_color)
        surface.blit(input_label, (20, y_offset))
        y_offset += input_label.get_height() + 10
        
        # Calculate input box dimensions for multi-line support
        input_box_width = self.popup_width - 40
        input_box_height = 170  # Increased height for multi-line
        input_box_rect = pygame.Rect(20, y_offset, input_box_width, input_box_height)
        pygame.draw.rect(surface, self.input_bg_color, input_box_rect)
        pygame.draw.rect(surface, self.input_border_color, input_box_rect, 2)
        
        # Wrap and render input text
        if self.player_answer:
            wrapped_input_lines = self._wrap_text(self.player_answer, self.input_font, input_box_width - 20)
            
            line_y = y_offset + 8
            for i, line in enumerate(wrapped_input_lines):
                if line_y + self.input_font.get_height() > y_offset + input_box_height - 8:
                    # If we're running out of space, show "..." to indicate more text
                    if i < len(wrapped_input_lines) - 1:
                        overflow_text = self.input_font.render("...", True, (150, 150, 150))
                        surface.blit(overflow_text, (25, line_y))
                    break
                
                input_text = self.input_font.render(line, True, self.text_color)
                surface.blit(input_text, (25, line_y))
                line_y += self.input_font.get_height() + 2
        
        # Cursor (show on last visible line)
        if self.player_answer:
            wrapped_input_lines = self._wrap_text(self.player_answer, self.input_font, input_box_width - 20)
            if wrapped_input_lines:
                # Calculate cursor position on the last visible line
                visible_lines = min(len(wrapped_input_lines), 
                                (input_box_height - 16) // (self.input_font.get_height() + 2))
                if visible_lines > 0:
                    last_line = wrapped_input_lines[visible_lines - 1]
                    cursor_x = 25 + self.input_font.size(last_line)[0]
                    cursor_y = y_offset + 8 + (visible_lines - 1) * (self.input_font.get_height() + 2)
                    if pygame.time.get_ticks() % 1000 < 500:  # Blinking cursor
                        pygame.draw.line(surface, self.text_color, 
                                    (cursor_x, cursor_y), 
                                    (cursor_x, cursor_y + self.input_font.get_height()), 2)
        else:
            # Show cursor at start if no text
            if pygame.time.get_ticks() % 1000 < 500:
                pygame.draw.line(surface, self.text_color, 
                            (25, y_offset + 8), 
                            (25, y_offset + 8 + self.input_font.get_height()), 2)
        
        y_offset += input_box_height + 20
        
        # Instructions
        instructions = [
            "Type your answer and press Enter to submit",
            f"Attempt {self.attempt_count + 1} of {self.max_attempts}",
            "Press Escape to cancel"
        ]
        
        for instruction in instructions:
            inst_surface = self.input_font.render(instruction, True, (200, 200, 200))
            inst_x = (self.popup_width - inst_surface.get_width()) // 2
            surface.blit(inst_surface, (inst_x, y_offset))
            y_offset += inst_surface.get_height() + 5
    
    def _draw_evaluating_screen(self, surface):
        """Draw the evaluating screen"""
        # Title
        title_text = self.title_font.render("Evaluating answer...", True, self.text_color)
        title_x = (self.popup_width - title_text.get_width()) // 2
        title_y = (self.popup_height - title_text.get_height()) // 2
        surface.blit(title_text, (title_x, title_y))
        
        # Loading animation (simple dots)
        dots = "." * ((pygame.time.get_ticks() // 500) % 4)
        loading_text = self.question_font.render(f"Please wait{dots}", True, (200, 200, 200))
        loading_x = (self.popup_width - loading_text.get_width()) // 2
        loading_y = title_y + title_text.get_height() + 20
        surface.blit(loading_text, (loading_x, loading_y))
    
    def _draw_result_popup(self, surface):
        """Draw the result popup with AI feedback"""
        if not self.quiz_result:
            return
        
        # Clear surface
        surface.fill(self.popup_bg_color)
        pygame.draw.rect(surface, self.border_color, 
                        (0, 0, self.popup_width, self.popup_height), 4)
        
        y_offset = 20
        
        # Title based on result
        if "Correct!" in self.quiz_result:
            title = "Correct Answer!"
            title_color = (100, 255, 100)
        elif "Maximum attempts" in self.quiz_result:
            title = "Quiz Failed"
            title_color = (255, 100, 100)
        else:
            title = "Try Again"
            title_color = (255, 200, 100)
        
        title_surface = self.title_font.render(title, True, title_color)
        title_x = (self.popup_width - title_surface.get_width()) // 2
        surface.blit(title_surface, (title_x, y_offset))
        y_offset += title_surface.get_height() + 20
        
        # Split text by newlines first, then wrap each paragraph
        paragraphs = self.quiz_result.split('\n')
        
        for paragraph in paragraphs:
            if paragraph.strip():  # Skip empty paragraphs
                # Wrap each paragraph individually
                wrapped_lines = self._wrap_text(paragraph, self.question_font, self.popup_width - 40)
                
                for line in wrapped_lines:
                    line_surface = self.question_font.render(line, True, self.text_color)
                    surface.blit(line_surface, (20, y_offset))
                    y_offset += line_surface.get_height() + 2
            else:
                # Add spacing for empty lines (like \n\n)
                y_offset += self.question_font.get_height() // 2
        
        # Show "Press Enter to continue" instead of countdown
        if "Try Again" in title:
            continue_text = "Press Enter to try again!"
        else:
            continue_text = "Press Enter to continue"
            
        continue_surface = self.input_font.render(continue_text, True, (150, 150, 150))
        continue_x = (self.popup_width - continue_surface.get_width()) // 2
        surface.blit(continue_surface, (continue_x, self.popup_height - 40))    
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
    
    def set_callbacks(self, completion_callback, failure_callback):
        """Set callbacks for quiz completion/failure"""
        self.completion_callback = completion_callback
        self.failure_callback = failure_callback
    
    def should_disable_main_game_elements(self):
        """Returns True if main game elements should be disabled during quiz"""
        return self.is_active
