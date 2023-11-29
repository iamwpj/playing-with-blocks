import numpy as np
from pathlib import Path
import sys

# Use this tool to sequentially process a file.

def open_saved_array(filename: Path) -> np.array:
    """Open saved array from a file.

    Args:
        filename (Path): Point to a saved "npy" file.

    Returns:
        np.array: The loaded data. If this is not an array, an exception will be raised.
    """

    with open(filename, 'rb') as f:
        return np.load(f)

    

class Organize():
    """The process of organizing blocks.
    """

    def __init__(self,prelim_array: np.array):
        self.prelim_array = prelim_array

    def _itemize(self):
        for i in self.prelim_array:
            print(f'{i}\n')


if __name__ == "__main__":
    if sys.argv[1]:
        Organize(open_saved_array(filename=Path(sys.argv[1]))).select_letters()
