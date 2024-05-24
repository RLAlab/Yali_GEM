#%%

import cobra

# Load the models
model_iYLI649 = cobra.io.read_sbml_model('/Users/giorgiadelmissier/Desktop/Yali_GEM/iYLI649/iYLI649.xml')
model_iYali = cobra.io.read_sbml_model('/Users/giorgiadelmissier/Desktop/Yali_GEM/iYali/iYali.xml')
model_iYli21 = cobra.io.read_sbml_model('/Users/giorgiadelmissier/Desktop/Yali_GEM/iYli21/iYli21.xml')

# Print the number of reactions
print(len(model_iYLI649.reactions))
print(len(model_iYali.reactions))
print(len(model_iYli21.reactions))
# %%

#iYLI649

for reaction in model_iYLI649.reactions[12:13]:
    print(f"Reaction ID: {reaction.id}")
    print(f"Reaction name: {reaction.name}")
    
    print(f"Reaction Equation: {reaction.build_reaction_string()}")

    if reaction.gene_reaction_rule:
        print(f"Gene Association: {reaction.gene_reaction_rule}")

    print("-" * 40)


# reaction IDs are from BiGG (http://bigg.ucsd.edu)

# %%

#iYali

# for reaction in model_iYali.reactions[15:17]:
#     print(f"Reaction ID: {reaction.id}")
#     print(f"Reaction name: {reaction.name}")
    
#     print(f"Reaction Equation: {reaction.build_reaction_string()}")

#     if reaction.annotation:
#         print("Cross-references (Annotations):")
#         for key, value in reaction.annotation.items():
#             print(f"  {key}: {value}")

#     if reaction.gene_reaction_rule:
#         print(f"Gene Association: {reaction.gene_reaction_rule}")

#     print("-" * 40)

# reaction ID is just a number, but some of them have some additional annotations, e.g.

rxn = model_iYali.reactions[15]

#print("\n\n\nReaction 13:\n")
print(f"Reaction ID: {rxn.id}")
print(f"Reaction name: {rxn.name}")
print(f"Reaction Equation: {rxn.build_reaction_string()}")
print(f"Gene Association: {rxn.gene_reaction_rule}")
print("Cross-references (Annotations):")
for key, value in rxn.annotation.items():
    print(f"  {key}: {value}")

# %%

#iYli21

# for reaction in model_iYli21.reactions[:5]:
#     print(f"Reaction ID: {reaction.id}")
#     print(f"Reaction name: {reaction.name}")
    
#     print(f"Reaction Equation: {reaction.build_reaction_string()}")

#     if reaction.annotation:
#         print("Cross-references (Annotations):")
#         for key, value in reaction.annotation.items():
#             print(f"  {key}: {value}")

#     if reaction.gene_reaction_rule:
#         print(f"Gene Association: {reaction.gene_reaction_rule}")

#     print("-" * 40)

rxn = model_iYli21.reactions[1487]

rxn = model_iYli21.reactions[3]

#print("\n\n\nReaction 1487:\n")
print(f"Reaction ID: {rxn.id}")
print(f"Reaction name: {rxn.name}")
print(f"Reaction Equation: {rxn.build_reaction_string()}")
print(f"Gene Association: {rxn.gene_reaction_rule}")
print("Cross-references (Annotations):")
for key, value in rxn.notes.items():
    print(f"  {key}: {value}")

# %%
