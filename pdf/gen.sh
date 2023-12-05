#!/usr/bin/env bash
#
# Generate a PDF of the readme.md
#
# Requires
#   - https://github.com/raghur/mermaid-filter

pandoc \
    -F mermaid-filter \
    -f gfm \
    -t html5 \
    --standalone \
    --metadata pagetitle="File System Analysis Toolkit for File Recovery" \
    --css github.css \
    ../readme.md -o project_3.pdf