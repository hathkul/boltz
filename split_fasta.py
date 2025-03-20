import argparse
import os
from Bio import SeqIO

def main():
    parser = argparse.ArgumentParser(
        description="Split a combined FASTA file into separate files with chain pairs."
    )
    parser.add_argument(
        "input_file",
        help="The combined FASTA file containing sequences (e.g., all_sequences.fasta)"
    )
    args = parser.parse_args()

    input_file = args.input_file

    # Dictionary to collect sequences by base name (e.g. nb_des_5_dldesign_0_best)
    records_by_file = {}

    # Parse the combined FASTA file
    with open(input_file, "r") as infile:
        for record in SeqIO.parse(infile, "fasta"):
            # Expected header format: nb_des_5_dldesign_0_best.pdb_H or ..._T
            parts = record.id.split(".pdb_")
            if len(parts) != 2:
                print(f"Unexpected header format: {record.id}")
                continue
            base = parts[0]  # e.g. nb_des_5_dldesign_0_best
            chain = parts[1] # expected to be 'H' or 'T'
            
            # Update the record header to the new format, e.g., >H|protein| or >T|protein|
            new_id = f"{chain}|protein|"
            record.id = new_id
            record.description = ""
            
            # Group records by the base name.
            if base not in records_by_file:
                records_by_file[base] = {}
            records_by_file[base][chain] = record

    # Create a FASTA file for each original PDB file that has both chains
    for base, chain_records in records_by_file.items():
        if "H" in chain_records and "T" in chain_records:
            output_filename = f"{base}.fasta"
            with open(output_filename, "w") as outfile:
                # Write H chain first, then T chain; change the order if desired.
                SeqIO.write([chain_records["H"], chain_records["T"]], outfile, "fasta")
            print(f"Wrote {output_filename}")
        else:
            print(f"Incomplete chain pair for {base}. Chains available: {list(chain_records.keys())}")

if __name__ == "__main__":
    main()
