#!/bin/bash
# This script runs "boltz predict <filename.fasta> --use_msa_server" for every FASTA file in the directory

for fasta in *.fasta; do
    if [[ -f "$fasta" ]]; then
        echo "Processing $fasta..."
        boltz predict "$fasta" --use_msa_server
    fi
done
