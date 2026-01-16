import csv
import math
import sys
from collections import Counter
from typing import Dict, List, Any, Tuple, Optional

# 1. Load data from CSV with error handling

def load_players(csv_path: str) -> List[Dict[str, Any]]:
    """
    Load player data from CSV file with error handling
    """
    players = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                print("CSV file is empty or invalid!")
                return players
            
            # Check required fields
            required_fields = ["name", "club", "position", "nationality", 
                              "retired", "ballon_dor", "champions_league"]
            missing_fields = [field for field in required_fields 
                            if field not in reader.fieldnames]
            
            if missing_fields:
                print(f"Missing fields: {missing_fields}")
                return players
            
            for row_num, row in enumerate(reader, 1):
                try:
                    players.append({
                        "name": row["name"].strip(),
                        "club": row["club"].strip(),
                        "position": row["position"].strip(),
                        "nationality": row["nationality"].strip(),
                        "retired": row["retired"].strip().lower() == "true",
                        "ballon_dor": row["ballon_dor"].strip().lower() == "true",
                        "champions_league": row["champions_league"].strip().lower() == "true"
                    })
                except KeyError as e:
                    print(f"Error in row {row_num}: missing field {e}")
                except Exception as e:
                    print(f"Error processing row {row_num}: {e}")
                    
    except FileNotFoundError:
        print(f"File {csv_path} not found!")
    except Exception as e:
        print(f"Error reading file: {e}")
    
    print(f"Loaded {len(players)} player(s)")
    return players


# 2. entropy calculation
def entropy(probs: List[float]) -> float:
    """
    Calculate entropy with special case handling
    """
    if not probs:
        return 0.0
    
    # Filter zero and negative values
    valid_probs = [p for p in probs if p > 0]
    
    if len(valid_probs) <= 1:
        return 0.0
    
    return -sum(p * math.log2(p) for p in valid_probs)


# 3. Information Gain calculation

def information_gain(players: List[Dict], state: Dict[str, float], 
                    attribute: str) -> float:
    """
    Calculate Information Gain with special case handling
    """
    if not players or not state:
        return 0.0
    
    # Base entropy values
    base_probs = list(state.values())
    if sum(base_probs) == 0:
        return 0.0
    
    base_entropy = entropy(base_probs)
    
    # Group players by attribute value
    value_groups = {}
    for p in players:
        val = p.get(attribute)
        if val is None:
            continue
        if attribute in ["retired", "ballon_dor", "champions_league"]:
            val = str(bool(val))
        else:
            val = str(val)
        value_groups.setdefault(val, []).append(p["name"])
    
    # If all values are the same, this question is useless
    if len(value_groups) <= 1:
        return 0.0
    
    # Calculate weighted entropy
    weighted_entropy = 0.0
    total_weight = sum(state.values())
    
    for val, names in value_groups.items():
        group_weight = sum(state.get(name, 0) for name in names)
        
        if group_weight == 0 or total_weight == 0:
            continue
        
        # Calculate probabilities within the group
        group_probs = [state[name] / group_weight for name in names if state.get(name, 0) > 0]
        
        if group_probs:
            weighted_entropy += (group_weight / total_weight) * entropy(group_probs)
    
    return max(0.0, base_entropy - weighted_entropy)


# 4. question selection

ATTRIBUTES = [
    "club",
    "position",
    "nationality",
    "retired",
    "ballon_dor",
    "champions_league"
]

def best_question(players: List[Dict], state: Dict[str, float]) -> Optional[Tuple[str, List[str]]]:
    """
    Select best question with possible answer values
    """
    if len(state) <= 1:
        return None
    
    gains = {}
    possible_answers = {}
    
    for attr in ATTRIBUTES:
        gain = information_gain(players, state, attr)
        if gain > 0:
            gains[attr] = gain
            
            # Collect unique values for this attribute
            if attr in ["retired", "ballon_dor", "champions_league"]:
                possible_answers[attr] = ["yes", "no"]
            else:
                # Collect actual values available in remaining players
                active_players = [p for p in players if state.get(p["name"], 0) > 0]
                unique_values = sorted(set(str(p[attr]) for p in active_players))
                if unique_values:
                    possible_answers[attr] = unique_values
    
    if not gains:
        return None
    
    best_attr = max(gains, key=gains.get)
    return best_attr, possible_answers.get(best_attr, [])


# 5. state update

def update_state(players: List[Dict], state: Dict[str, float], 
                attribute: str, answer: Any) -> Dict[str, float]:
    """
    Update probability state based on answer
    """
    # Convert text answer to appropriate value
    if isinstance(answer, str):
        answer_lower = answer.lower().strip()
        if answer_lower in ["yes", "true", "y"]:
            answer_bool = True
        elif answer_lower in ["no", "false", "n"]:
            answer_bool = False
        else:
            answer_bool = answer_lower
    
    new_state = {}
    for p in players:
        player_name = p["name"]
        current_prob = state.get(player_name, 0)
        
        if current_prob == 0:
            continue
        
        # Compare values considering attribute type
        if attribute in ["retired", "ballon_dor", "champions_league"]:
            player_value = bool(p[attribute])
            answer_value = answer_bool if isinstance(answer, str) else bool(answer)
            matches = player_value == answer_value
        else:
            player_value = str(p[attribute]).lower()
            answer_value = str(answer).lower()
            matches = player_value == answer_value
        
        if matches:
            new_state[player_name] = current_prob
        else:
            new_state[player_name] = 0.0
    
    # Normalize probabilities
    total = sum(new_state.values())
    if total > 0:
        for name in new_state:
            new_state[name] /= total
    
    return new_state


# 6. Helper functions

def display_possible_players(state: Dict[str, float], players: List[Dict], 
                           limit: int = 5) -> None:
    """
    Display possible players with their probabilities
    """
    active_players = [(name, prob) for name, prob in state.items() if prob > 0]
    
    if not active_players:
        print("No matching players found!")
        return
    
    # Sort by probability
    active_players.sort(key=lambda x: x[1], reverse=True)
    
    print("\n" + "="*50)
    print("Possible Players:")
    print("="*50)
    
    for i, (name, prob) in enumerate(active_players[:limit], 1):
        # Find player information
        player_info = next((p for p in players if p["name"] == name), {})
        club = player_info.get("club", "Unknown")
        position = player_info.get("position", "Unknown")
        nationality = player_info.get("nationality", "Unknown")
        
        print(f"{i}. {name} ({club}, {position}, {nationality})")
        print(f"   Probability: {prob:.1%}")
    
    if len(active_players) > limit:
        print(f"... and {len(active_players) - limit} more player(s)")


def get_user_input(prompt: str, valid_options: List[str] = None) -> str:
    """
    Get user input with validation
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input:
                print("Please enter a value!")
                continue
                
            if valid_options:
                # Convert input for better matching
                user_lower = user_input.lower()
                for option in valid_options:
                    if user_lower == option.lower():
                        return option
                
                # For yes/no answers
                if user_lower in ["yes", "y", "true"]:
                    return "yes"
                elif user_lower in ["no", "n", "false"]:
                    return "no"
                
                print(f"Please enter a valid answer. Options: {valid_options}")
            else:
                return user_input
                
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)
        except Exception as e:
            print(f"Input error: {e}")


# 7. main engine

def run_engine(csv_path: str) -> None:
    """
    Main game engine with enhanced interface
    """
    print("="*60)
    print("Welcome to the Player Guessing Engine!")
    print("="*60)
    
    # Load data
    players = load_players(csv_path)
    if not players:
        print("Could not load player data. Check players.csv file")
        return
    
    # Initialize state
    initial_prob = 1.0 / len(players)
    state = {p["name"]: initial_prob for p in players}
    
    max_questions = 20  # Maximum number of questions
    questions_asked = 0
    
    print(f"\nLoaded {len(players)} player(s) to start!")
    print(f"You can answer 'yes' or 'no' for binary questions, or enter a specific value for others")
    print("Type 'quit' to exit at any time\n")
    
    while questions_asked < max_questions:
        # Display current statistics
        active_count = sum(1 for prob in state.values() if prob > 0)
        print(f"\n{'='*30}")
        print(f"Question: {questions_asked + 1}")
        print(f"Remaining players: {active_count}")
        
        if active_count == 0:
            print("No players match the criteria!")
            break
        elif active_count == 1:
            winner = next(name for name, prob in state.items() if prob > 0)
            print(f"\n🎉 The player you're thinking of is: {winner} 🎉")
            break
        
        # Choose best question
        question_result = best_question(players, state)
        if not question_result:
            print("Cannot select a new question!")
            break
        
        question_attr, possible_answers = question_result
        
        # Format question in a user-friendly way
        question_texts = {
            "club": "Does the player play for club",
            "position": "Does the player play in position",
            "nationality": "Is the player's nationality",
            "retired": "Is the player retired?",
            "ballon_dor": "Has the player won Ballon d'Or?",
            "champions_league": "Has the player won Champions League?"
        }
        
        question_text = question_texts.get(question_attr, f"value {question_attr}")
        
        if question_attr in ["retired", "ballon_dor", "champions_league"]:
            print(f"\nQuestion: {question_text}")
            answer = get_user_input("Answer (yes/no): ", ["yes", "no"])
            answer_bool = answer == "yes"
        else:
            # Display available options to user
            print(f"\nQuestion: {question_text}")
            if possible_answers:
                print(f"Available options: {', '.join(possible_answers[:10])}")
                if len(possible_answers) > 10:
                    print(f"... and {len(possible_answers) - 10} more options")
            
            answer = get_user_input("Answer: ")
        
        # Update state
        if question_attr in ["retired", "ballon_dor", "champions_league"]:
            state = update_state(players, state, question_attr, answer_bool)
        else:
            state = update_state(players, state, question_attr, answer)
        
        # Display possible players
        display_possible_players(state, players)
        
        questions_asked += 1
        
        # Check for certainty
        best_player = max(state, key=state.get, default=None)
        confidence = state.get(best_player, 0) if best_player else 0
        
        if confidence > 0.95:
            player_info = next((p for p in players if p["name"] == best_player), {})
            print(f"\n{'='*60}")
            print(f"🎯 I'm {confidence:.1%} confident!")
            print(f"The player you're thinking of is: {best_player}")
            if player_info:
                print(f"Club: {player_info.get('club')}")
                print(f"Position: {player_info.get('position')}")
                print(f"Nationality: {player_info.get('nationality')}")
            print("="*60)
            break
    
    if questions_asked >= max_questions:
        print("\nReached maximum number of questions!")
        if best_player and confidence > 0:
            print(f"Best guess: {best_player} (confidence: {confidence:.1%})")
    
    print("\nThank you for using the Player Guessing Engine!")


# 8) Main function

def main():
    """
    Main function with error handling
    """
    try:
        csv_file = "players.csv"
        run_engine(csv_file)
    except KeyboardInterrupt:
        print("\n\nProgram stopped.")
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        print("Error details:", sys.exc_info())


# 9. Run the program

if __name__ == "__main__":
    main()