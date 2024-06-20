#%%

import cobra

# Load the models
model_iYLI649 = cobra.io.read_sbml_model('models/iYLI649.xml')
model_iYali = cobra.io.read_sbml_model('models/iYali.xml')
model_iYli21 = cobra.io.read_sbml_model('models/iYli21.xml')

# %%

#find exchange reaction involving carbon sources

carbon_sources = ['glucose', 'glycerol', 'fructose', 'galactose', 'formate', 'xylose']

for model in [model_iYLI649, model_iYali, model_iYli21]:
    print(f"Model: {model}")
    for i,r in enumerate(model.reactions):
        if 'exchange' in r.name.lower():
            if any(s in r.name.lower() for s in carbon_sources):
                print(f"Reaction at index {i}: {r.name}, {r.id}")

    print('---' * 10)

# %%

# find biomass objective function

for model in [model_iYLI649, model_iYali, model_iYli21]:
    print(f"Model: {model}")
    print(f"Objective function: {model.objective}")
    print('---' * 10)

biomass_iYLI649 = model_iYLI649.reactions.get_by_id('biomass_carbon_limiting')
biomass_iYali = model_iYali.reactions.get_by_id('xBIOMASS')
biomass_iYli21 = model_iYli21.reactions.get_by_id('biomass_C')

# %%

# For example, the first reactant in biomass_iYLI649 is 13BDglcn_c (1_3_beta_D_Glucan)

# You find all the reactions involving this metabolite:
metabolite = model_iYLI649.metabolites.get_by_id('13BDglcn_c')
reactions_involving_metabolite = metabolite.reactions

for reaction in reactions_involving_metabolite:
    print(reaction.name)

#%%
# You have the mapping of each reaction name between the models
# In this case we know that:

# Reaction 12 from iYLI649:
# Reaction ID: 13GS
# Reaction name: 1 3 beta glucan synthase
# Reaction Equation: udpg_c --> 13BDglcn_c + h_c + udp_c
# Gene Association: YALI0C01411g and YALI0E21021g

# Reaction 15 from iYali:
# Reaction ID: y000005
# Reaction name: 1,3-beta-glucan synthase
# Reaction Equation: s_1543 --> s_0001 + s_0794 + s_1538
# Gene Association: YALI0C01411g or YALI0E21021g
# Cross-references (Annotations):
#   sbo: SBO:0000176
#   ec-code: 2.4.1.34
#   kegg.reaction: R03118
#   pubmed: 7649185

# Reaction 3 from iYli21:
# Reaction ID: R4
# Reaction name: 1,3-beta-glucan synthase
# Reaction Equation: m8[C_cy] --> m10[C_cy] + m11[C_cy] + m9[C_en]
# Gene Association: YALI1C01944g or YALI1E25018g
# Cross-references (Annotations):
#   PROTEIN_CLASS: 2.4.1.34

# Therefore, we can map each metabolite name between the models:

metabolite = model_iYali.metabolites.get_by_id('s_0001')
print(metabolite.name)

metabolite = model_iYli21.metabolites.get_by_id('m9[C_en]')
print(metabolite.name)

# 13BDglcn_c in iYLI649 is:
#     - s_0001 in iYali
#     - m9[C_en] in iYli21


# You do this for each reactant and product in the biomass reactions, and once you have all the mappings
# you can rewrite the biomass equations using the corresponding nomenclature 
# and exchange the biomass reactions between the models