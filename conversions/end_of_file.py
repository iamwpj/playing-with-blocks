end_of_file = {
    # This is "Document" -- a phrase commonly embedded at/near
    # the end of Microsoft Word Documents.
    "MS Office File": b"\x44\x6F\x63\x75\x6D\x65\x6E\x74",
    # This is "%%EOF" it will additionally match empty space
    # so we don't mis-match.
    "PDF": b"\x25\x25\x45\x4F\x46\x0D\x0A\x00",
    # This will search for a common ending of JPEG files and match
    # it with space padding (00).
    "JPEG": b"\xFF\xD9\x00\x00",
}
