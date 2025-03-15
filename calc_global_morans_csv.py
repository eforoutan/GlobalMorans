import geopandas as gpd
import sys
import csv
from libpysal.weights import Queen, Rook
from esda.moran import Moran

def calc_global_morans(input_shapefile, field_name, weight_type='queen'):
    """
    Parameters:
    - input_shapefile (str): Path to the input shapefile
    - field_name (str): Name of the field/column to calculate Moran's I
    - weight_type (str): Type of spatial weights ('queen' or 'rook')

    Returns:
    tuple: Moran's I, Z-score, P-value
    """
    # Load the shapefile
    try:
        shapefile_data = gpd.read_file(input_shapefile)
    except Exception as e:
        print(f"Failed to read shapefile: {e}")
        return None

    # Check if the field exists in the shapefile
    if field_name not in shapefile_data.columns:
        print(f"Field '{field_name}' not found in the shapefile attributes.")
        return None

    # Create a spatial weights matrix
    if weight_type.lower() == 'queen':
        weights = Queen.from_dataframe(shapefile_data)
    elif weight_type.lower() == 'rook':
        weights = Rook.from_dataframe(shapefile_data)
    else:
        print("Invalid weight type specified. Use 'queen' or 'rook'.")
        return None

    # Handle missing values
    shapefile_data[field_name] = shapefile_data[field_name].fillna(shapefile_data[field_name].mean())

    # Calculate Moran's I
    moran = Moran(shapefile_data[field_name], weights)

    # Return the results
    return (moran.I, moran.z_norm, moran.p_norm)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Incorrect number of arguments provided.")
        sys.exit(1)

    input_shapefile = sys.argv[1]
    field_name = sys.argv[2]
    weight_type = sys.argv[3]

    results = calc_global_morans(input_shapefile, field_name, weight_type)

    if results:
        # Write results to CSV
        output_csv = "global_morans_results.csv"
        with open(output_csv, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["Field", "Global Moran's I", "Z-score", "P-value"])
            writer.writeheader()
            writer.writerow({
                "Field": field_name,
                "Global Moran's I": results[0],
                "Z-score": results[1],
                "P-value": results[2]
            })
        print(f"Results successfully written to {output_csv}")
    else:
        print("Calculation failed.")
