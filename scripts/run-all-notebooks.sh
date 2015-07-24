#!/bin/sh
NOTEBOOKS=$(find notebooks -name '*.ipynb' -maxdepth 1)
for nb in $NOTEBOOKS; do
    echo $nb
    ipython nbconvert $nb \
        --ExecutePreprocessor.enabled=True \
        --ExecutePreprocessor.timeout=180 \
        --to notebook \
        --output $nb
    echo >> $nb # Add newline at end of file
done
