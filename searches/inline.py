# These should have ordering specified.
# There are 794 potential blocks for any file so if you need this
# later, simply go above that number.
# Multiples will replace eachother.
inline_matches = {
    # These are constructed by looking at functional files.
    "MS Office File": [
        (
            # [Content_Types].xml -- used for theming. Appears early.
            # b"\x5B\x43\x6F\x6E\x74\x65\x6E\x74\x5F\x54\x79\x70\x65\x73\x5D\x2E\x78\x6D\x6C\xAC",
            b"\x2E\x78\x6D\x6C",
            1,
        ),
    ],
    "PDF": [
        (
            # Matches "/Pag"[e][s] (shortened to be even length)
            b"\x2F\x50\x61\x67",
            8,
        ),
        (
            # Matches "/Roo"[t] ((shortened to be even length))
            b"\x2F\x52\x6F\x6F",
            9,
        ),
        (
            # Matches [0]"0000 n" (shortened to be even length)
            b"\x30\x30\x30\x30\x20\x6E",
            10,
        ),
        (
            # Matches "xref"
            b"\x78\x72\x65\x66",
            99,
        ),
        (
            # Matches ">> /" -- common formatters in PDF
            b"\x3E\x3E\x20\x2F",
            199,
        ),
        (
            # Matches "endstrea"[m] (shortened to be even length)
            b"\x65\x6E\x64\x73\x74\x72\x65\x61",
            200,
        ),
        (
            # Matches "/Produce"[r] (shortened to be even length)
            b"\x2F\x50\x72\x6F\x64\x75\x63\x65",
            798,
        ),
        (
            # This matches against what's already in the trailer -- always at the end.
            b"\x20\x36\x35\x35\x33\x35\x20\x66",
            799,
        ),
    ],
    "JPEG": [
        (
            # This denotes the end of a thumbnail. It should only find valid results
            # since it's being found after the standard endmatter.
            b"\xFF\xD9",
            1,
        )
    ],
}