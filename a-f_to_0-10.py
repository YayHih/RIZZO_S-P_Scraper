import csv

# Function to translate letter grades (including + and -) to numeric scores
def translate_scores(input_file, output_file):
    # Mapping for base letter grades
    base_score_mapping = {
        "A": 100,
        "B": 85,
        "C": 75,
        "D": 65,
        "F": 0
    }

    # Adjustments for + and -
    modifier_mapping = {
        "+": 5,
        "-": -5
    }

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Score Numeric']  # Add a new column for numeric scores
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # Write header row
        writer.writeheader()

        # Process each row
        for row in reader:
            score = row['Score'].strip()  # Get the score
            numeric_score = None  # Default value for unscored entries
            
            # Check if the score is mappable
            if score in ["Not Scored", "Not Available"]:
                numeric_score = None
            else:
                base_score = base_score_mapping.get(score[0])  # Get base score for the first letter
                if base_score is not None:
                    # Check for modifiers
                    if len(score) > 1 and score[1] in modifier_mapping:
                        numeric_score = base_score + modifier_mapping[score[1]]
                    else:
                        numeric_score = base_score

            row['Score Numeric'] = numeric_score
            writer.writerow(row)

# Input and output file paths
input_filepath = "cdp_esg_reports.csv"  # Replace with your input file name
output_filepath = "numericalized_cdp.csv"  # Replace with your desired output file name

# Run the translation
translate_scores(input_filepath, output_filepath)

print(f"Translated scores saved to {output_filepath}")
