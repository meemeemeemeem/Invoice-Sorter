# Invoice-Sorter
 A small script to sort PDF invoices by date on a vendor by vendor basis. Requires the datetime and tika modules.
 
 # Usage
 
 First, add all invoices for a month into a folder, separated into subfolders for each merchant. Then run the script, using the folder containing all of the month's invoices for the first input, and the year the invoices are in a four-digit format (leave empty to use the current year). Then, the script will add a 2-digit padded number and hyphen at the beginning of the file name to sort the invoices into date order from earliest to latest (e.g. 01 - Invoice1.pdf). This script will only scan pdf files, and will ignore any files starting with ".\_", containing the word "statement" (not case sensitive), and any non-text pdf files.
