import string
import random
import re

def display_status():
    status = "Currently selected: "
    status += ", ".join([f"{option_texts[o]}" for o in sorted(selected_options)])
    print("\n" + status + "\n")

def evaluate_password_strength(passwd, selected_types):
    # Base score on length
    length_score = 0
    if len(passwd) >= 8:
        length_score += 1
    if len(passwd) >= 12:
        length_score += 2
    if len(passwd) >= 16:
        length_score += 3
    
    # Diversity checks based on selected character sets
    diversity_score = len(selected_types)  # Up to 3 points for using all types
    
    # Additional checks for character diversity within the password
    has_lower = any(char.islower() for char in passwd)
    has_upper = any(char.isupper() for char in passwd)
    has_digit = any(char.isdigit() for char in passwd)
    has_special = any(char in string.punctuation for char in passwd)
    char_types_score = sum([has_lower, has_upper, has_digit, has_special])
    
    # Adjust score based on the actual mix of characters used
    actual_diversity_score = char_types_score / 2  # Max 2 points here for having all types

    # Penalties for common patterns or sequences
    pattern_penalty = 0
    if re.search(r'(123|pass|qwerty|abc|111|000|admin|welcome)', passwd.lower()):
        pattern_penalty += 3
    if re.search(r'(\w)\1{2,}', passwd):
        pattern_penalty += 2  # Repeated characters penalty

    # Total score calculation
    total_score = length_score + diversity_score + actual_diversity_score - pattern_penalty

    # Get strength based on points
    if total_score >= 8:
        return 'Super Strong'
    elif total_score >= 6:
        return 'Very Strong'
    elif total_score >= 4:
        return 'Strong'
    elif total_score >= 2:
        return 'Moderate'
    else:
        return 'Weak'

# Initialize variables and descriptions
length = int(input("Enter password length (8 or more recommended): "))
print("\nChoose character sets for your password. A good password contains a mix of the following:\n")

option_texts = {1: "Digits (0-9)", 2: "Letters (a-zA-Z)", 3: "Special characters (!@#$...)"}
character_sets = {1: string.digits, 2: string.ascii_letters, 3: string.punctuation}
characterList = ""
selected_options = set()

# Main loop for user options
while True:
    print('''Options:
    1. Add Digits (0-9)
    2. Add Letters (a-zA-Z)
    3. Add Special Characters (!@#$...)
    4. Remove a Character Set
    5. Generate Password\n''')
    display_status()
    choice = int(input("Select an option (1-5): "))

    if choice in [1, 2, 3]:
        if choice in selected_options:
            print(f"\nYou've already included {option_texts[choice]}.\n")
        else:
            characterList += character_sets[choice]
            selected_options.add(choice)
            print(f"\nAdded {option_texts[choice]}.\n")
    elif choice == 4:
        if selected_options:
            remove_choice = int(input("Enter the option number to remove (1-3): "))
            if remove_choice in selected_options:
                characterList = characterList.replace(character_sets[remove_choice], "")
                selected_options.remove(remove_choice)
                print(f"\nRemoved {option_texts[remove_choice]}.\n")
            else:
                print("\nOption not selected or invalid, nothing to remove.\n")
        else:
            print("\nNo options to remove.\n")
    elif choice == 5:
        if len(selected_options) >= 1:
            break
        else:
            print("\nSelect at least one character set before generating a password.\n")
    else:
        print("\nPlease pick a valid option!\n")

# Password generation with prevention of consecutive identical characters
password = []
previous_char = None
if characterList:
    while len(password) < length:
        randomchar = random.choice(characterList)
        if randomchar != previous_char:  # Prevent consecutive identical characters
            password.append(randomchar)
            previous_char = randomchar

    # Displaying the final output
    final_password = "".join(password)
    print("\nYour new password is: " + final_password)
    print("Password Strength: " + evaluate_password_strength(final_password, selected_options) + "\n")
else:
    print("\nNo characters selected for password generation.\n")
