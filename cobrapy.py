#%%

import cobra

# Load the models
model_iYLI649 = cobra.io.read_sbml_model('models/iYLI649.xml')
model_iYali = cobra.io.read_sbml_model('models/iYali.xml')
model_iYli21 = cobra.io.read_sbml_model('models/iYli21.xml')

# Stats
print("Total number of reactions:")
for model in [model_iYLI649, model_iYali, model_iYli21]:
    print(f"{model}: {len(model.reactions)}")

print("Total number of genes:")
for model in [model_iYLI649, model_iYali, model_iYli21]:
    print(f"{model}: {len(model.genes)}")

print("Total number of metabolites:")
for model in [model_iYLI649, model_iYali, model_iYli21]:
    print(f"{model}: {len(model.metabolites)}")
# %%

print("Examples:\n")

#iYLI649

rxn = model_iYLI649.reactions[12]
print("Reaction 12 from iYLI649:")
print(f"Reaction ID: {rxn.id}")
print(f"Reaction name: {rxn.name}")
print(f"Reaction Equation: {rxn.build_reaction_string()}")
print(f"Gene Association: {rxn.gene_reaction_rule}")
print("--" * 40 + "\n")

# reaction IDs are from BiGG (http://bigg.ucsd.edu)

#iYali

rxn = model_iYali.reactions[15]
print("Reaction 15 from iYali:")
print(f"Reaction ID: {rxn.id}")
print(f"Reaction name: {rxn.name}")
print(f"Reaction Equation: {rxn.build_reaction_string()}")
print(f"Gene Association: {rxn.gene_reaction_rule}")
print("Cross-references (Annotations):")
for key, value in rxn.annotation.items():
    print(f"  {key}: {value}")
print("--" * 40 + "\n")

# reaction ID is just a number, but some of them have some additional annotations

#iYli21

rxn = model_iYli21.reactions[3]
print("Reaction 3 from iYli21:")
print(f"Reaction ID: {rxn.id}")
print(f"Reaction name: {rxn.name}")
print(f"Reaction Equation: {rxn.build_reaction_string()}")
print(f"Gene Association: {rxn.gene_reaction_rule}")
print("Cross-references (Annotations):")
for key, value in rxn.notes.items():
    print(f"  {key}: {value}")
print("--" * 40)

# reaction ID is just a number, but some of them have some additional annotations

# %%
