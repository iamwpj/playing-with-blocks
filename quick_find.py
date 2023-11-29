#!/usr/bin/env python

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
import sys

block = f"blockset/{sys.argv[1]}"
search_term = bytes.fromhex(sys.argv[2])

debug = False


search_np = np.frombuffer(search_term, dtype=np.uint8)
f = open(block, "rb")
src_np = np.fromfile(f, dtype=np.uint8)

win_len = len(search_np)

slw = sliding_window_view(src_np, window_shape=win_len)

tot_c = len(slw)
row_c = 0

# This will provide a Tuple of (*real* location, data)
found = []
for row in slw:
    row_c += 1
    res = np.equal(row, search_np)
    if all(res):
        print(f"Search:\t{search_np.tobytes()}")
        print(f"Found:\t{row.tobytes()}")
        print(f"Row:\t{row_c}/{tot_c}")

        # Print the location to find at in the file (this is basically the row counter).
        row_location = row_c if row_c % 2 == 0 else row_c - 1
        print(f"Find starting at byte {row_location} in original hex data.")


if found and debug:
    row_c = 0
    for row in slw:
        row_c += 1
        print(f"{row_c}:\t{row.tobytes()}")
