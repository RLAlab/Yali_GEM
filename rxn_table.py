# %%

import cobra
import re
import pandas as pd
from rapidfuzz import process, fuzz

# Load the models
model_iYLI649 = cobra.io.read_sbml_model('models/iYLI649.xml')
model_iYali = cobra.io.read_sbml_model('models/iYali.xml')
model_iYli21 = cobra.io.read_sbml_model('models/iYli21.xml')

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

#%%

df1 = pd.DataFrame(matches_iYLI649_iYali).transpose().reset_index()
df1.columns = ['iYLI649_ID', 'iYLI649_Name', 'iYali_ID', 'iYali_Name']

df2 = pd.DataFrame(matches_iYLI649_iYli21).transpose().reset_index()
df2.columns = ['iYLI649_ID', 'iYLI649_Name', 'iYli21_ID', 'iYli21_Name']

df3 = pd.DataFrame(matches_iYali_iYli21).transpose().reset_index()
df3.columns = ['iYali_ID', 'iYali_Name', 'iYli21_ID', 'iYli21_Name']

df = df1.merge(df2, on=['iYLI649_ID', 'iYLI649_Name'], how='outer').merge(df3, on=['iYali_ID', 'iYali_Name'], how='outer')
df.drop(columns=['iYli21_ID_y', 'iYli21_Name_y'], inplace=True)
df.columns = ['iYLI649_ID', 'iYLI649_Name', 'iYali_ID', 'iYali_Name', 'iYli21_ID', 'iYli21_Name']
# %%

# Create a set of all reaction ids from all models
all_reactions = set(reactions_iYLI649 + reactions_iYali + reactions_iYli21)

# Create a set of all reaction ids already in the DataFrame
existing_reactions = set(df[['iYLI649_ID', 'iYLI649_Name']].itertuples(index=False, name=None)) | \
                     set(df[['iYali_ID', 'iYali_Name']].itertuples(index=False, name=None)) | \
                     set(df[['iYli21_ID', 'iYli21_Name']].itertuples(index=False, name=None))

# Identify reactions not already in the DataFrame
missing_reactions = all_reactions - existing_reactions

# Add missing reactions to the DataFrame with NaNs for missing columns
for reaction_id, reaction_name in missing_reactions:
    new_row = {
        'iYLI649_ID': reaction_id if (reaction_id, reaction_name) in reactions_iYLI649 else None,
        'iYLI649_Name': reaction_name if (reaction_id, reaction_name) in reactions_iYLI649 else None,
        'iYali_ID': reaction_id if (reaction_id, reaction_name) in reactions_iYali else None,
        'iYali_Name': reaction_name if (reaction_id, reaction_name) in reactions_iYali else None,
        'iYli21_ID': reaction_id if (reaction_id, reaction_name) in reactions_iYli21 else None,
        'iYli21_Name': reaction_name if (reaction_id, reaction_name) in reactions_iYli21 else None
    }
    df = df.append(new_row, ignore_index=True)

# Save the DataFrame to a CSV file
df.to_csv('rxn_table.tsv', sep="\t")
# %%
