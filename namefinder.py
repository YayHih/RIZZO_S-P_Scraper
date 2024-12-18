def create_security_type_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Open the output file to save the extracted data
    with open(output_file, 'w') as out_f:
        out_f.write("Security|Industry|Sub-Industry|State\n")  # Header row

        # Skip the header row and start processing
        for line in lines:
            parts = line.strip().split('\t')
            if len(parts) >= 5:  # Ensure there are enough columns to extract required fields
                security_name = parts[1].strip()  # Second column is the Security Name
                industry = parts[2].strip()       # Third column is the Industry
                sub_industry = parts[3].strip()   # Fourth column is the Sub-Industry
                state = parts[4].strip()          # Fifth column is the State
                
                # Write the extracted data to the output file
                out_f.write(f"{security_name}|{industry}|{sub_industry}|{state}\n")

# File paths
input_filepath = "sandptest.txt"  # Replace with your input file's name
output_filepath = "security_type.txt"

# Run the function
create_security_type_file(input_filepath, output_filepath)

print(f"{output_filepath} successfully created with Security, Industry, Sub-Industry, and State info.")
