import pandas as pd
import cobra


# Define the data
data = {
    "Glucose uptake rate (mmol·gDCW⁻¹·h⁻¹)": [2.43, 0.61, 0.64],
    "Experiment (h⁻¹)": [0.26, 0.047, 0.048],
    "iYli21 (h⁻¹)": [0.28, 0.031, 0.036],
    "iYali4 (h⁻¹)": [0.18, 0.020, 0.022]
}

# Create a DataFrame
df = pd.DataFrame(data)
print(df)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

# Plot each line
plt.plot(df["Glucose uptake rate (mmol·gDCW⁻¹·h⁻¹)"], df["Experiment (h⁻¹)"], marker='o', label='Experiment')
plt.plot(df["Glucose uptake rate (mmol·gDCW⁻¹·h⁻¹)"], df["iYli21 (h⁻¹)"], marker='x', label='iYli21')
plt.plot(df["Glucose uptake rate (mmol·gDCW⁻¹·h⁻¹)"], df["iYali4 (h⁻¹)"], marker='^', label='iYali4')

plt.xlabel('Glucose uptake rate (mmol·gDCW⁻¹·h⁻¹)')
plt.ylabel('Specific growth rate (h⁻¹)')
plt.title('Comparison of Experiment and Model Predictions')
plt.legend()
plt.show()


# Load the model
model_path = "C:/Users/SAYANTAN DE/Downloads/gems/iYli21/iYli21.xml"
model = cobra.io.read_sbml_model(model_path)

# Function to simulate growth rate for a given glucose uptake rate
def simulate_growth_rate(model, uptake_rate):
    try:
        # Set the glucose uptake rate
        reaction = model.reactions.get_by_id('R1070')
        reaction.lower_bound = -uptake_rate  # uptake
        reaction.upper_bound = 0             # no secretion

        print(f"Set glucose uptake rate to {-uptake_rate}")

        # Perform FBA
        solution = model.optimize()
        
        if solution.status != 'optimal':
            print(f"No optimal solution found for uptake rate {uptake_rate}")
            return None
        
        print(f"Growth rate for uptake rate {uptake_rate}: {solution.objective_value}")
        return solution.objective_value
    except Exception as e:
        print(f"Error with uptake rate {uptake_rate}: {e}")
        return None

# Test the model with the glucose uptake rates from the data
glucose_uptake_rates = df["Glucose uptake rate (mmol·gDCW⁻¹·h⁻¹)"]
predicted_growth_rates = [simulate_growth_rate(model, rate) for rate in glucose_uptake_rates]

predicted_growth_rates
