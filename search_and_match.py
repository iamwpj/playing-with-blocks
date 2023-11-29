#!/usr/bin/env python

from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from conversions.file_exts import file_exts
from conversions.signatures import signatures
from conversions.end_of_file import end_of_file
from searches.inline import inline_matches
from searches.character_types import character_types

import mixmaster as mm


@dataclass(init=True, repr=True)
class OrderedBlocks:
    """This will provide blocks with a sequence"""

    id: str
    parent: str
    block: np.ndarray
    order: int or str = 1


@dataclass(init=True, repr=True)
class Found:
    """Use this to structure found items."""

    id: str
    file_path: Path
    signature: bytes
    signature_name: str
    block: np.ndarray
    endmatter: bytes = None
    endmatter_name: str = None
    child_blocks: Optional[List[OrderedBlocks]] = None

    def __post_init__(self):
        # Set as list if not set already.
        if not isinstance(self.child_blocks, list):
            self.child_blocks = []


def matchmaker(search_in: np.ndarray, search_for: np.ndarray) -> bool:
    """Use a sliding window to compare ndarrays
       https://numpy.org/devdocs/reference/generated/numpy.lib.stride_tricks.sliding_window_view.html#numpy-lib-stride-tricks-sliding-window-view

    Args:
        search_in (np.ndarray): The array you're going to search in.
        search_for (np.ndarray): The array you're going to search for.

    Returns:
        bool: True if found, False if not found.
    """

    win_len = len(search_for)

    if (win_len % 2) != 0:
        raise ValueError(
            f"`search_for` MUST be an even length. Provided {search_for}:{win_len}"
        )

    search_arr = sliding_window_view(search_in, window_shape=win_len)

    results = []
    for row in search_arr:
        results.append(all(np.equal(row, search_for)))

    if any(results):
        return True
    else:
        return False


def save(filename: Path, data: np.array):
    """Save array to file

    Args:
        filename (Path): Provide a destination to save in.
        data (np.array): Provide the data array.
    """

    with open(filename, "wb+") as f:
        np.save(f, data)


def combinator(filename: Path, block: Found):
    """Finally, a way to see it all together

    Args:
        filename (Path): Provide a filename to write to.
        blocks (Found): An object of a found item. This assumes your list is ordered.
    """

    with open(filename, "wb+") as f:
        # Start with initial data (header)
        ordered = [block.block]

        # Then add ordering
        [
            ordered.insert(cb.order, cb.block)
            for cb in block.child_blocks
            if cb.order != "end"
        ]

        # Append the end block
        [ordered.append(cb.block) for cb in block.child_blocks if cb.order == "end"]

        # Append ordered to output and write.
        output = np.vstack(ordered)
        save(filename, output)
        print(f"\tWrote {len(output)*512} bytes to {filename}")


byte_blocks = []

source_blocks = Path("./blockset").glob("BLOCK*")

for block in source_blocks:
    byte_blocks.append((block, np.fromfile(block.absolute(), dtype="uint8")))

sig_items = [
    (name, np.frombuffer(sig, dtype=np.uint8))
    for name in signatures
    for sig in signatures[name]
]


# Let's find headers.

header_hits = []
for sig_name, sig in sig_items:
    for n, b in byte_blocks:
        if all(np.isin(sig, b[: len(sig)])):
            header_hits.append(
                Found(
                    id=n.name,
                    file_path=n,
                    signature=sig,
                    signature_name=sig_name,
                    block=b,
                    child_blocks=[],
                )
            )

            print(f"HEADER\tMatched: {[hex(x) for x in sig]}\t{n.name}.")

            # Do not match this to any other potential files.
            byte_blocks.remove((n, b))


# Let's process our header hits as singular files.

for hit in header_hits:
    # Find endmatter
    hit.endmatter = (
        np.frombuffer(end_of_file[hit.signature_name], dtype=np.uint8)
        if hit.signature_name in list(end_of_file.keys())
        else None
    )
    hit.endmatter_name = hit.signature_name if hit.endmatter is not None else None

    if hit.endmatter is not None and hit.signature_name:
        # This is always the first child block. It means after this the list
        # can be updated with `inserts`

        for n, b in byte_blocks:
            if matchmaker(search_in=b, search_for=hit.endmatter):
                print(f"END\tMatched: {[hex(x) for x in hit.endmatter]}\t{n.name}")
                hit.child_blocks.append(
                    OrderedBlocks(id=n.name, parent=hit.id, block=b, order="end")
                )

                # We don't need to search this one anymore since sectors are
                # also file ends -- meaning once a file has ended in a sector,
                # no new data would be written there.
                byte_blocks.remove((n, b))

    # Search for inline

    for search_term, order in inline_matches[hit.signature_name]:
        search_term = np.frombuffer(search_term, dtype=np.uint8)
        for n, b in byte_blocks:
            if matchmaker(search_in=b, search_for=search_term):
                print(
                    f"INLINE\tMatched: {[hex(x) for x in search_term]}\t{n.name}: {order}:{hit.id}"
                )
                hit.child_blocks.append(
                    OrderedBlocks(id=n.name, parent=hit.id, block=b, order=order)
                )

                # We only assign one block to one parent. It's going to cause
                # some headaches for images.
                byte_blocks.remove((n, b))

    # Search for character objects
    if hit.signature_name in character_types.keys():
        for n, b in byte_blocks:
            for rule in character_types[hit.signature_name].rules:
                nonempty = np.array(b[np.argwhere(b != 255)])
                found_values = np.array(
                    nonempty[
                        np.where(
                            np.logical_and(nonempty >= rule.start, nonempty <= rule.end)
                        )
                    ]
                )
                found_match_percent = (len(found_values) / len(nonempty)) * 100
                if found_match_percent >= rule.match_percent:
                    print(
                        f"INLINE\tMatched: {character_types[hit.signature_name].rule_name}\t{n.name}: {rule.order}:{hit.id}:{found_match_percent}% matched"
                    )
                    hit.child_blocks.append(
                        OrderedBlocks(
                            id=n.name, parent=hit.id, block=b, order=rule.order
                        )
                    )

                    # We only assign one block to one parent. It's going to cause
                    # some headaches for images.
                    byte_blocks.remove((n, b))
                else:
                    print(
                        f"INLINE\tFAILED: {character_types[hit.signature_name].rule_name}\t{n.name}: {rule.order}:{hit.id}:{found_match_percent}% matched"
                    )
    # Write output

    combinator(
        filename=f"./test_out/run-{hit.id}.{file_exts[hit.signature_name]}.npy",
        block=hit,
    )
