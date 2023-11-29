# https://en.wikipedia.org/wiki/List_of_file_signatures
signatures = {
    "MS Office File": [b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1"],
    "PDF": [b"\x25\x50\x44\x46\x2D"],
    # The JPEG files are going to be found inside the PDF,
    # but they won't start at the begining of a sector like
    # a traditional JPEG file would.
    "JPEG": [
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46",
        b"\x49\x46\x00\x01",
        b"\xFF\xD8\xFF\xE0",
    ],
}
