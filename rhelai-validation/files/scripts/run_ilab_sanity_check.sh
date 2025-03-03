#!/bin/bash

# Run the ilab_sanity_check.py script inside the iLab shell
ILAB_ADDITIONAL_MOUNTS="/tmp/scripts:/scripts" ilab shell << EOF
python /scripts/ilab_sanity_check.py
exit \$?
EOF
