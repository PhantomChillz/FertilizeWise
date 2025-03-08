import pandas as pd
import random

def get_npk_values(soil_type):
    try:
        # Load the dataset
        file_path = "C:\\Users\\rushi\\Desktop\\FertilizeWIseDjagno\\FertWiseMergedMain.csv"
        df = pd.read_csv(file_path)

        # Normalize column names (strip spaces)
        df.columns = df.columns.str.strip()

        # Check if "Soil_Type" exists
        if "Soil_Type" not in df.columns:
            return None, "Error: 'Soil_Type' column not found."

        # Filter data for the given soil type
        filtered_df = df[df["Soil_Type"].str.lower() == soil_type.lower()]

        # Check if soil type exists in the dataset
        if filtered_df.empty:
            return None, f"Soil type '{soil_type}' not found in dataset."

        # Get min and max for Nitrogen, Phosphorous, Potassium
        n_min, n_max = filtered_df["Nitrogen"].min(), filtered_df["Nitrogen"].max()
        p_min, p_max = filtered_df["Phosphorous"].min(), filtered_df["Phosphorous"].max()
        k_min, k_max = filtered_df["Potassium"].min(), filtered_df["Potassium"].max()

        # Generate random values within the range
        random_n = random.randint(n_min, n_max)
        random_p = random.randint(p_min, p_max)
        random_k = random.randint(k_min, k_max)

        return {
            'nitrogen': random_n,
            'phosphorous': random_p,
            'potassium': random_k
        }, None

    except Exception as e:
        return None, f"Error: {str(e)}"