#!/bin/awk -f

# Set field separator as comma for csv and print the HTML header line
BEGIN {
    FS=";"
    print "<table id='passportoffices'>"
	print "<thead>"
	print "<tr>"
	print "<th scope=\"col\"><b>Facility</b></th>"
	print "<th scope=\"col\"><b>Address</b></th>"
	print "<th scope=\"col\"><b>City</b></th>"
	print "<th scope=\"col\"><b>State</b></th>"
	print "<th scope=\"col\"><b>ZIP</b></th>"
	print "<th scope=\"col\"><b>Phone</b></th>"
	print "</tr>"
	print "</thead>"	
	print "<tbody>"
}
# Function to print a row with one argument to handle either a 'th' tag or 'td' tag
function printRow(tag) {
    print "<tr>";
    for(i=1; i<=NF; i++) print "<"tag">"$i"</"tag">";
    print "</tr>"
}
# If CSV file line number (NR variable) is 1, call printRow fucntion with 'th' as argument
# NR==1 {
#     printRow("th")
# }
# If CSV file line number (NR variable) is greater than 1, call printRow fucntion with 'td' as argument
NR>1 {
    printRow("td")
}
# Print HTML footer
END {
	print "</tbody>"
	print "</table>"
}
