# File System Analysis Toolkit for File Recovery

When analyzing the imaged copies, we often encounter some scenarios that we have a number of imaged blocks (disk sectors), but the indexing block (e.g., UNIX inode) has been eliminated/destroyed, assuming that there is no pointer information in these imaged blocks. The question is how to design and develop a toolkit to help to recover these files by first classifying the blocks into a number of sets according to file signatures. And then for each set of blocks, the toolkit should find the correct sequence of these sectors and reconstruct the file (possibly a part of the file). The file format supported by this toolkit can be MS WORD, PDF, JPEG, TIF, TXT, etc.  You can use Encase or other tools to create your own data set, or use the set of imaged disk sectors we provide. The toolkit can be run on Linux or Windows systems.

The imaged disk sectors file [CP3-3-blockset.zip](https://www.engineering.iastate.edu/~guan/course/CprE-536/courseproject920/CP3-3-blockset.zip) we provide here contains 899 randomly indexed blocks, each of which has size 512 bytes. These blocks belong to three different files: 
* one PDF
* one WORD
* one JPEG 

_There is no unallocated block._

Please develop a toolkit which can classify these blocks into three sets correctly. Furthermore, if you can find the correct sequence of these blocks and reconstruct the files, you can get 3 bonus points.

* Filename = [CP3-3-blockset.zip](https://www.engineering.iastate.edu/~guan/course/CprE-536/courseproject920/CP3-3-blockset.zip)
* MD5 sum = 017c90727e8dfcb757ae189cacc74c18

# Resources

- https://en.wikipedia.org/wiki/List_of_file_signatures
- Finding a MS Office file in hex: https://www.youtube.com/watch?v=W22wnNUXqGM

## JPEG

### Identifying

- https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format
- https://www.w3.org/Graphics/JPEG/jfif3.pdf

### Testing

- Testing JPEG: https://www.kokkonen.net/tjko/src/man/jpeginfo.txt 
- https://stackoverflow.com/questions/1401527/how-do-i-programmatically-check-whether-an-image-png-jpeg-or-gif-is-corrupte/1401565#1401565

## PDF

### Identifying

- https://www.oreilly.com/library/view/developing-with-pdf/9781449327903/ch01.html#example_1-12