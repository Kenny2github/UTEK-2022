@echo off
if "%2"=="" goto errormsg
echo on
py -m optimizer %1 < inputs\%1%2.in.txt > outputs\%1%2.out.txt
@goto end
:errormsg
echo Usage: %0 [part number] [output letter label, a/b/c]
echo All arguments are required.
:end