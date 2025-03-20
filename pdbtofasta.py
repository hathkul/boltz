import argparse
import os
from Bio.PDB import PDBParser, PPBuilder

def main():
    parser = argparse.ArgumentParser(
        description="Extract protein sequences from PDB files in a folder and output them to a FASTA file."
    )
    parser.add_argument("pdb_folder", help="Path to the folder containing PDB files")
    parser.add_argument(
        "-o", "--output", default="all_sequences.fasta",
        help="Output FASTA file name (default: all_sequences.fasta)"
    )
    args = parser.parse_args()

    pdb_folder = args.pdb_folder
    output_fasta = args.output

    pdb_parser = PDBParser(QUIET=True)
    ppb = PPBuilder()

    with open(output_fasta, "w") as fasta_out:
        # Loop through each file in the folder
        for pdb_file in os.listdir(pdb_folder):
            if pdb_file.endswith(".pdb"):
                filepath = os.path.join(pdb_folder, pdb_file)
                structure = pdb_parser.get_structure(pdb_file, filepath)
                # Iterate over all models (usually there's one, but can be more)
                for model in structure:
                    # Iterate over each chain in the model
                    for chain in model:
                        sequence = ""
                        # Extract continuous peptide segments
                        for pp in ppb.build_peptides(chain):
                            sequence += str(pp.get_sequence())
                        # Write to FASTA if a sequence was found
                        if sequence:
                            fasta_out.write(f">{pdb_file}_{chain.id}\n")
                            fasta_out.write(sequence + "\n")
                            print(f"Extracted sequence for chain {chain.id} from {pdb_file}")

if __name__ == "__main__":
    main()
