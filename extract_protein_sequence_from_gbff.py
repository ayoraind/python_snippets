import os
import argparse
from Bio import SeqIO

def extract_protein_sequences(parent_directory, gene_name, output_directory):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Iterate over the directories in the parent directory
    for dirpath, dirnames, filenames in os.walk(parent_directory):
        for filename in filenames:
            if filename.endswith('.gbff'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r') as gbff_file:
                    for record in SeqIO.parse(gbff_file, 'genbank'):
                        for feature in record.features:
                            if feature.type == 'CDS' and 'product' in feature.qualifiers:
                                product = feature.qualifiers['product'][0]
                                if gene_name in product:
                                    if 'translation' in feature.qualifiers:
                                        accession = record.id
                                        protein_sequence = feature.qualifiers['translation'][0]

                                        # Create the output filename based on the original GBFF filename
                                        output_filename = f"{os.path.splitext(filename)[0]}.fasta"
                                        output_filepath = os.path.join(output_directory, output_filename)

                                        # Write the protein sequence to the output file
                                        with open(output_filepath, 'a') as output_file:
                                            output_file.write(f">{accession}\n")
                                            output_file.write(f"{protein_sequence}\n\n")

# Create the argument parser
parser = argparse.ArgumentParser(description='Scan GBFF files for a named gene and extract protein sequences.')

# Add the positional arguments
parser.add_argument('parent_directory', help='Path to the parent directory containing subdirectories with GBFF files')
parser.add_argument('gene_name', help='Name of the gene to search for')
parser.add_argument('output_directory', help='Path to the output directory for the FASTA files')

# Parse the arguments
args = parser.parse_args()

# Call the function to extract the protein sequences and save them into FASTA files
extract_protein_sequences(args.parent_directory, args.gene_name, args.output_directory)
