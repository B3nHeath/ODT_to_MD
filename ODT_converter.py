from odf import text, teletype
from odf.opendocument import load
import os
from mdutils.mdutils import MdUtils
from mdutils import Html

# Change directory to home (this will probably be changed in the long-term)
os.chdir('/home/ben')
# Collect the odt file of interest
ODT_file = input("File: ")

## Initialise variables for later use
# Text storage
text_content = []
# List of headers to check for
headers = ["Article title:", "Authors:", "Journal:", "Date of Publication:", "URL:", "My Synopsis:", "1) What is the central argument that the authors want to make?", "2) What is the method that the authors use to make that argument?", "3) What results do the authors obtain from their method?", "4) What conclusions do the authors draw from their results?", "5) What counter-arguments, limitations, or alternative perspectives can shed light on the argument, method, results, or conclusions?", "Reflections:" ]
# Header storage
header_position = {}
# Position tracker
i = -1

# Load the ODT file
doc = load(ODT_file)

# For each line in odt file
for element in doc.getElementsByType(text.P):
    # Track the list position
    i +=1
    # Extract the text
    text = teletype.extractText(element)
    # Check if each of the headers in our headers list is present within the text
    for header in headers:
        if header in text:
            # If yes, update our dictionary to record the header, and its position in the text
            header_position.update({header: i})
            # Then strip the header itself from the text, and any whitespace
            text = text.lstrip(header).strip()
    # Append the line of text to our text list
    if text != "":
        text_content.append(text)

## These are our checkers so that we know what we are playing with
# print(header_position)
# print(text_content)

# Then change the directory to the test position we place our markdown files into
os.chdir('Documents/MD_Test/ODT_readings')

# Create a filename, based on the 1st line of text (should be title of journal/book)
file_name = text_content[0] + ".md"

# Create and write the new file (note this will raise file error if the file name already exists)
with open(file_name, "x") as file:
    # Write a title header
    file.write(f"# Title: \n\n{text_content[header_position['Article title:']]}\n\n")
    header_position.pop("Article title:")
    # Write the content from the title in our dictionary (Note: This will break if it is not present, but it should be in all our cases). Its also a little bit inefficient, I get an error when I add it all into the writer above (something to do with the quotes?)
    # For each of the first 4 headers in our complete potential list
    for header in headers[1:4]:
        # If it is found in the document
        if header in header_position:
            # Write it as a 2nd heading along with the content of the text
            file.write(f"## {header} \n\n{text_content[header_position[header]]}\n\n")
            header_position.pop(header)
    # If there is a URL
    if header_position["URL:"]:
        # Write the sub-heading, and add the link into the document
        file.write(f"## URL:\n\n[link]({text_content[header_position['URL:']]})\n\n")
        header_position.pop("URL:")

######## Begin notes section ########
    file.write("# Notes\n\n")
    # Create a list of the present headers
    header_keys = list(header_position.keys())
    # For each of the present headers, excluding the last one (so we don't fall out of index range)
    # Create a header value, and its position in the list
    for position, header in enumerate(header_keys[:-1]):
        # Write the header as a 2nd header
        file.write(f"## {header}\n\n")
        # For text in the range between the header and the next header
        for text in text_content[header_position[header]:header_position[header_keys[position+1]]]:
            # Write each sentence with a double-break between
            file.write(f"{text}\n\n")
    # Then write the final header
    file.write(f"## {header_keys[-1]}\n\n")
    # And the text associated with the final header
    for text in text_content[header_position[header_keys[-1]]:]:
        file.write(f"{text}\n\n")