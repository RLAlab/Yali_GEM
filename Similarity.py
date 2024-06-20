from fuzzywuzzy import fuzz, process

# Define the reaction sets
set1 = [
    "asparagine synthase glutamine hydrolysing", "Asparaginyl tRNA synthetase",
    "asparaginyl tRNA synthetase miotchondrial", "asparagine mitochondrial transport via proton transport",
    "L asparagine reversible transport via proton symport", "aspartate 1 decarboxylase",
    "Isocitrate dehydrogenase NAD", "aspartate glutamate peroxisomal shuttle",
    "Isocitrate dehydrogenase NADP", "aspartate transaminase", "aspartate transaminase",
    "aspartate transaminase peroxisomal", "Aspartyl tRNA synthetase",
    "Aspartyl tRNA synthetase mitochondrial", "aspartate mitochondrial transport via proton symport"
]

set2 = [
    "asparagine synthase (glutamine-hydrolysing)", "Asparaginyl-tRNA synthetase",
    "asparaginyl-tRNA synthetase, miotchondrial", "aspartate carbamoyltransferase",
    "aspartate kinase", "aspartate transaminase", "aspartate transaminase",
    "aspartate transaminase", "aspartate-semialdehyde dehydrogenase", "Aspartyl-tRNA synthetase"
]

set3 = [
    "asparagine synthase (glutamine-hydrolysing)", "Asparaginyl-tRNA synthetase",
    "asparaginyl-tRNA synthetase, miotchondrial", "aspartate carbamoyltransferase",
    "aspartate kinase", "aspartate transaminase", "aspartate transaminase",
    "aspartate transaminase", "aspartate-semialdehyde dehydrogenase", "Aspartyl-tRNA synthetase",
    "Aspartyl-tRNA synthetase"
]

# Function to find matches between sets with a given threshold
def find_matches(set_a, set_b, threshold=90):
    matches = {}
    for item in set_a:
        match = process.extractOne(item, set_b, scorer=fuzz.token_sort_ratio)
        if match and match[1] >= threshold:
            matches[item] = match[0]
    return matches

# Function to find matches between three sets
def find_common_in_three(set_a, set_b, set_c, threshold=90):
    common_ab = find_matches(set_a, set_b, threshold)
    common_bc = find_matches(set_b, set_c, threshold)
    
    common_abc = {}
    for item in common_ab:
        match = process.extractOne(item, set_c, scorer=fuzz.token_sort_ratio)
        if match and match[1] >= threshold:
            common_abc[item] = match[0]
    
    return common_abc

# Find matches between all sets
matches_1_2 = find_matches(set1, set2)
matches_1_3 = find_matches(set1, set3)
matches_2_3 = find_matches(set2, set3)
matches_1_2_3 = find_common_in_three(set1, set2, set3)

# Function to find common matches among all three sets
def find_common_matches(matches_1_2, matches_1_3, matches_2_3):
    common_matches = set(matches_1_2.keys()) & set(matches_1_3.keys())
    common_reactions = {item: matches_1_2[item] for item in common_matches if item in matches_2_3}
    return common_reactions

# Get the common matches
common_reactions = find_common_matches(matches_1_2, matches_1_3, matches_2_3)

# Print the results
print(f"Matches between set 1 and set 2: {matches_1_2}")
print(f"Matches between set 1 and set 3: {matches_1_3}")
print(f"Matches between set 2 and set 3: {matches_2_3}")
print(f"Matches between set 1,2 and set 3: {matches_1_2_3}")
print(f"Number of shared reaction names: {len(common_reactions)}")
print(f"Shared reaction names: {common_reactions}")

# Print the number of common reaction names between each pair of sets
print(f"Number of common reactions between set 1 and set 2: {len(matches_1_2)}")
print(f"Number of common reactions between set 2 and set 3: {len(matches_2_3)}")
print(f"Number of common reactions between set 1 and set 3: {len(matches_1_3)}")
print(f"Number of common reactions between set 1, set 2, and set 3: {len(matches_1_2_3)}")
