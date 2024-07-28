#%%
import xml.etree.ElementTree as ET

def update_biomass_stoichiometry(xml_file, reaction_id, new_stoichiometry, output_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Define the namespaces
    namespaces = {
        'sbml': 'http://www.sbml.org/sbml/level3/version1/core',
        'fbc': 'http://www.sbml.org/sbml/level3/version1/fbc/version2'
    }

    # Register the namespaces to avoid adding ns0 prefixes
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)

    # Find the reaction with the given ID
    reaction = root.find(f".//sbml:reaction[@id='{reaction_id}']", namespaces)
    if reaction is None:
        print(f"Reaction {reaction_id} not found.")
        return

    # Update reactants
    list_of_reactants = reaction.find('sbml:listOfReactants', namespaces)
    for species_ref in list_of_reactants.findall('sbml:speciesReference', namespaces):
        species = species_ref.get('species')
        if species in new_stoichiometry['reactants']:
            species_ref.set('stoichiometry', str(new_stoichiometry['reactants'][species]))

    # Update products
    list_of_products = reaction.find('sbml:listOfProducts', namespaces)
    for species_ref in list_of_products.findall('sbml:speciesReference', namespaces):
        species = species_ref.get('species')
        if species in new_stoichiometry['products']:
            species_ref.set('stoichiometry', str(new_stoichiometry['products'][species]))

    # Save the modified XML to a new file
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Updated stoichiometric coefficients saved to {output_file}")

# Example usage
xml_file = r'C:\Users\SAYANTAN DE\Downloads\gems\iYli21.xml'
reaction_id = 'biomass_C'  # ID of the biomass reaction
new_stoichiometry = {
    'reactants': {
        'm9__91__C_en__93__': 0.281481,
        'm114__91__C_cy__93__': 0.0978466971830986,
        'm86__91__C_cy__93__': 0.0482,
        'm310__91__C_cy__93__': 0.0192387579617834,
        'm319__91__C_cy__93__': 0.0296749403508772,
        'm267__91__C_cy__93__': 0.0296749403508772,
        'm141__91__C_cy__93__': 23.09,
        'm401__91__C_cy__93__': 0.259113,
        'm95__91__C_cy__93__': 0.0368,
        'm443__91__C_cy__93__': 0.000586501941747573,
        'm89__91__C_cy__93__': 0.00138578247734139,
        'm459__91__C_cy__93__': 0.00143552442996743,
        'm465__91__C_cy__93__': 0.00127004610951009,
        'm505__91__C_cy__93__': 0.00142451552795031,
        'm1046__91__C_ex__93__': 0.035250723,
        'm130__91__C_cy__93__': 0.03822801328125,
        'm50__91__C_cy__93__': 0.03822801328125,
        'm272__91__C_cy__93__': 0.0922042789473684,
        'm93__91__C_cy__93__': 0.0593,
        'm32__91__C_cy__93__': 23.09,
        'm615__91__C_cy__93__': 0.00837798759124088,
        'm743__91__C_cy__93__': 0.0144341761061947,
        'm775__91__C_cy__93__': 0.0310067486725664,
        'm793__91__C_cy__93__': 0.0430828868217054,
        'm1324__91__C_cy__93__': 0.07037,
        'm74__91__C_cy__93__': 0.00691714122137404,
        'm378__91__C_em__93__': 5.774757e-05,
        'm1632__91__C_em__93__': 0.00034648544,
        'm1633__91__C_em__93__': 0.00023676505,
        'm859__91__C_cy__93__': 0.0127394605442177,
        'm765__91__C_cy__93__': 0.0336301422680412,
        '': 3.464854e-05,
        'm897__91__C_vm__93__': 7.507185e-05,
        'm441__91__C_cy__93__': 0.0472167770114943,
        'm964__91__C_cy__93__': 0.02,
        'm770__91__C_cy__93__': 0.034092602970297,
        'm294__91__C_cy__93__': 0.002047,
        '': 0.00023403363,
        'm772__91__C_cy__93__': 0.000324783333333333,
        'm992__91__C_cy__93__': 0.0063003981595092,
        'm149__91__C_cy__93__': 0.0397,
        'm1008__91__C_cy__93__': 0.0280691535353535,
        'm359__91__C_cy__93__': 0.003029289
    },
    'products': {
        'm143__91__C_cy__93__': 23.09,
        'm10__91__C_cy__93__': 23.09,
        'm35__91__C_cy__93__': 23.09
    }
}
output_file = r'C:\Users\SAYANTAN DE\Downloads\modified_iYli21.xml'

update_biomass_stoichiometry(xml_file, reaction_id, new_stoichiometry, output_file)

#%%

import xml.etree.ElementTree as ET

# Path to the input and output XML files
input_file_path = r'C:\Users\SAYANTAN DE\Downloads\gems\iYali.xml'
output_file_path = r'C:\Users\SAYANTAN DE\Downloads\modified_iYali.xml'

# Parse the XML file
tree = ET.parse(input_file_path)
root = tree.getroot()

# Namespace map (if any)
ns = {'': 'http://www.sbml.org/sbml/level3/version1/core'}

# Find the reaction with id="R_xBIOMASS"
reaction = root.find(".//reaction[@id='R_xBIOMASS']", ns)
if reaction is not None:
    list_of_reactants = reaction.find('listOfReactants', ns)
    list_of_products = reaction.find('listOfProducts', ns)

    # Clear the existing reactants and products
    list_of_reactants.clear()
    list_of_products.clear()

    # New stoichiometry data
    reactants = {
        "M_s_0001": 0.281481,
        "M_s_0955": 0.0978466971830986,
        "M_s_0423": 0.0482,
        "M_s_0965": 0.0192387579617834,
        "M_s_0969": 0.0296749403508772,
        "M_s_0973": 0.0296749403508772,
        "M_s_0434": 23.09,
        "M_s_0509": 0.259113,
        "M_s_0526": 0.0368,
        "M_s_0981": 0.000586501941747573,
        "M_s_0584": 0.00138578247734139,
        "M_s_0589": 0.00143552442996743,
        "M_s_0615": 0.00127004610951009,
        "M_s_0649": 0.00142451552795031,
        "M_s_0668": 0.035250723,
        "M_s_0999": 0.03822801328125,
        "M_s_0991": 0.03822801328125,
        "M_s_1003": 0.0922042789473684,
        "M_s_0782": 0.0593,
        "M_s_0803": 23.09,
        "M_s_1006": 0.00837798759124088,
        "M_s_1016": 0.0144341761061947,
        "M_s_1021": 0.0310067486725664,
        "M_s_1025": 0.0430828868217054,
        "M_s_1107": 0.07037,
        "M_s_1029": 0.00691714122137404,
        "M_m378": 5.774757e-05,
        "M_s_3711": 0.00034648544,
        "M_s_3712": 0.00023676505,
        "M_s_1032": 0.0127394605442177,
        "M_s_1035": 0.0336301422680412,
        "M_m897": 7.507185e-05,
        "M_s_1039": 0.0472167770114943,
        "M_s_1467": 0.02,
        "M_s_1045": 0.034092602970297,
        "M_s_1520": 0.002047,
        "M_s_1048": 0.000324783333333333,
        "M_s_1051": 0.0063003981595092,
        "M_s_1545": 0.0397,
        "M_s_1056": 0.0280691535353535,
        "M_s_1569": 0.003029289,
    }

    products = {
        "M_s_0394": 23.09,
        "M_s_0794": 23.09,
        "M_s_1322": 23.09
    }

    # Add new reactants
    for species, stoich in reactants.items():
        species_reference = ET.SubElement(list_of_reactants, 'speciesReference')
        species_reference.set('species', species)
        species_reference.set('stoichiometry', str(stoich))
        species_reference.set('constant', 'true')

    # Add new products
    for species, stoich in products.items():
        species_reference = ET.SubElement(list_of_products, 'speciesReference')
        species_reference.set('species', species)
        species_reference.set('stoichiometry', str(stoich))
        species_reference.set('constant', 'true')

    # Save the modified XML to a new file
    tree.write(output_file_path)
    print(f"Modified XML file has been saved to: {output_file_path}")
else:
    print("Reaction 'R_xBIOMASS' not found in the XML file.")

#%%