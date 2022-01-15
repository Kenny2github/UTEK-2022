# Optimizer
A project for UTEK 2022.

## Usage
Run the following commands while in the root of the project.

### Windows
```
run <part number> <part letter>
```
For example `run 3 b` to run from `inputs\3b.in.txt`.

### Linux
```
./run <part number> <part letter>
```
For example `./run 3 b` to run from `inputs/3b.in.txt`

### Python
```
<python> -m optimizer <part number> [input filename] [output filename]
```
If `[input filename]` is unspecified, input is read from `stdin`. You can redirect input from files with `(above command) < (filename)`.
If `[output filename]` is unspecified, output is printed to `stdout`. You can redirect output to files with `(above command) > (filename)`.
Note that some extraneous informational output is printed to `stderr`, which is not captured by either of the above methods (and will thus be safely excluded from being written to the file).