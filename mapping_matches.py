import cobra
from rapidfuzz import process, fuzz
import re

# Define file paths
iYLI649_path = 'C:\\Users\\SAYANTAN DE\\Downloads\\gems\\iYLI649.xml'
iYali_path = 'C:\\Users\\SAYANTAN DE\\Downloads\\gems\\iYali.xml'
iYli21_path = 'C:\\Users\\SAYANTAN DE\\Downloads\\gems\\iYli21.xml'

# Function to load a model and handle errors
def load_model(file_path):
    try:
        model = cobra.io.read_sbml_model(file_path)
        return model
    except Exception as e:
        print(f"Error loading model from {file_path}: {e}")
        return None

# Load the models
model_iYLI649 = load_model(iYLI649_path)
model_iYali = load_model(iYali_path)
model_iYli21 = load_model(iYli21_path)

# Function to extract reaction names and ids from a model
def get_reactions(model):
    return [(reaction.id, reaction.name) for reaction in model.reactions] if model else []

# Extract reaction names and ids
reactions_iYLI649 = get_reactions(model_iYLI649)
reactions_iYali = get_reactions(model_iYali)
reactions_iYli21 = get_reactions(model_iYli21)

# Function to extract digits from a string
def extract_digits(s):
    return ''.join(re.findall(r'\d', s))

# Function to clean and normalize reaction names for comparison
def normalize_name(name):
    return re.sub(r'\W+', '', name).lower()

# Function to find matches between sets with a given threshold and digit constraint
def find_matches(set_a, set_b, threshold=90):
    matches = {}
    for id_a, name_a in set_a:
        normalized_name_a = normalize_name(name_a)
        item_digits = extract_digits(name_a)
        candidates = [(id_b, name_b) for id_b, name_b in set_b if extract_digits(name_b) == item_digits]
        
        # Find the match with the highest score
        best_match = None
        best_score = 0
        for id_b, name_b in candidates:
            score = fuzz.token_sort_ratio(normalized_name_a, normalize_name(name_b))
            if score > best_score:
                best_match = (id_b, name_b)
                best_score = score
        
        if best_match and best_score >= threshold:
            matches[(id_a, name_a)] = best_match
    
    return matches

# Function to find matches between three sets
def find_common_in_three(set_a, set_b, set_c, threshold=90):
    common_ab = find_matches(set_a, set_b, threshold)
    common_bc = find_matches(set_b, set_c, threshold)
    
    common_abc = {}
    for (id_a, name_a) in common_ab:
        normalized_name_a = normalize_name(name_a)
        item_digits = extract_digits(name_a)
        candidates = [(id_c, name_c) for id_c, name_c in set_c if extract_digits(name_c) == item_digits]
        
        # Find the match with the highest score
        best_match_b = common_ab[(id_a, name_a)]
        best_match_c = None
        best_score = 0
        for id_c, name_c in candidates:
            score = fuzz.token_sort_ratio(normalized_name_a, normalize_name(name_c))
            if score > best_score:
                best_match_c = (id_c, name_c)
                best_score = score
        
        if best_match_c and best_score >= threshold:
            common_abc[(id_a, name_a)] = (best_match_b, best_match_c)
    
    return common_abc

# Find matches between all sets
matches_iYLI649_iYali = find_matches(reactions_iYLI649, reactions_iYali)
matches_iYLI649_iYli21 = find_matches(reactions_iYLI649, reactions_iYli21)
matches_iYali_iYli21 = find_matches(reactions_iYali, reactions_iYli21)
matches_all_three = find_common_in_three(reactions_iYLI649, reactions_iYali, reactions_iYli21)

# Define the output file path
output_file_path = 'C:\\Users\\SAYANTAN DE\\Downloads\\reaction_matches.txt'

# Save the results to a text file
with open(output_file_path, 'w') as file:
    file.write("Reaction names in iYLI649:\n")
    for id_649, name_649 in reactions_iYLI649:
        file.write(f"{name_649} ({id_649})\n")
    
    file.write("\nReaction names in iYali:\n")
    for id_yali, name_yali in reactions_iYali:
        file.write(f"{name_yali} ({id_yali})\n")
    
    file.write("\nReaction names in iYli21:\n")
    for id_yli21, name_yli21 in reactions_iYli21:
        file.write(f"{name_yli21} ({id_yli21})\n")

    file.write("\nMatches between iYLI649 and iYali:\n")
    for (id_649, name_649), (id_yali, name_yali) in matches_iYLI649_iYali.items():
        file.write(f"{name_649} ({id_649}) <-> {name_yali} ({id_yali})\n")
    
    file.write("\nMatches between iYLI649 and iYli21:\n")
    for (id_649, name_649), (id_yli21, name_yli21) in matches_iYLI649_iYli21.items():
        file.write(f"{name_649} ({id_649}) <-> {name_yli21} ({id_yli21})\n")
    
    file.write("\nMatches between iYali and iYli21:\n")
    for (id_yali, name_yali), (id_yli21, name_yli21) in matches_iYali_iYli21.items():
        file.write(f"{name_yali} ({id_yali}) <-> {name_yli21} ({id_yli21})\n")
    
    file.write("\nMatches among iYLI649, iYali, and iYli21:\n")
    for (id_649, name_649), ((id_yali, name_yali), (id_yli21, name_yli21)) in matches_all_three.items():
        file.write(f"{name_649} ({id_649}) <-> {name_yali} ({id_yali}) <-> {name_yli21} ({id_yli21})\n")
    
    file.write(f"\nNumber of shared reaction names: {len(matches_all_three)}\n")
    file.write(f"Number of common reactions between iYLI649 and iYali: {len(matches_iYLI649_iYali)}\n")
    file.write(f"Number of common reactions between iYali and iYli21: {len(matches_iYali_iYli21)}\n")
    file.write(f"Number of common reactions between iYLI649 and iYli21: {len(matches_iYLI649_iYli21)}\n")
    file.write(f"Number of common reactions among iYLI649, iYali, and iYli21: {len(matches_all_three)}\n")

print(f"Results have been written to {output_file_path}")

# Print the numbers
print(f"Number of shared reaction names: {len(matches_all_three)}")
print(f"Number of common reactions between iYLI649 and iYali: {len(matches_iYLI649_iYali)}")
print(f"Number of common reactions between iYali and iYli21: {len(matches_iYali_iYli21)}")
print(f"Number of common reactions between iYLI649 and iYli21: {len(matches_iYLI649_iYli21)}")
print(f"Number of common reactions among iYLI649, iYali, and iYli21: {len(matches_all_three)}")

# Print the total number of reaction names in each model
print(f"Total number of reaction names in iYLI649: {len(reactions_iYLI649)}")
print(f"Total number of reaction names in iYali: {len(reactions_iYali)}")
print(f"Total number of reaction names in iYli21: {len(reactions_iYli21)}")