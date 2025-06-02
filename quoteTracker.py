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
        
    def print_quote_status(self, username):
        """Print locked and unlocked quotes to console for MVP"""
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

    def show_quote_tracker_popup(self, username):
        """Show quote tracker popup (for now, just console output - will be UI later)"""
        if not username:
            print("QuoteTracker: Must be signed in to view quote tracker")
            return
            
        print("\n" + "="*50)
        print("🏆 QUOTE TRACKER ACTIVATED 🏆")
        print("="*50)
        self.print_quote_status(username)