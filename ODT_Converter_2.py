import glob
from odf import text, teletype
from odf.opendocument import load
import os

def main():
    path = input("Path: ")
    rec = input("Recursive (Y or N)? ")

    if rec == "Y":
        for file in glob.iglob("**/*.odt", root_dir = path, recursive=True):
            cont, header = reader(file, path)
            try:
                write_md(header, cont)
            except ValueError:
                print(file)
                pass



    else:
        for file in glob.iglob("*.odt", root_dir = path, recursive = False):
            cont, header = reader(file, path)
            write_md(header, cont)
            # Read and write the file in MD


def reader(file, path):
    text_content = []
    # List of headers to check for
    headers = ["Article title:", "Authors:", "Journal:", "Date of Publication:", "URL:", "My Synopsis:", "1) What is the central argument that the authors want to make?", "2) What is the method that the authors use to make that argument?", "3) What results do the authors obtain from their method?", "4) What conclusions do the authors draw from their results?", "5) What counter-arguments, limitations, or alternative perspectives can shed light on the argument, method, results, or conclusions?", "Reflections:" ]
    # Header storage
    header_position = {}
    # Position tracker
    i = -1

    # Load the ODT file
    doc = load(path + "/" + file)
    # For each line in odt file
    for element in doc.getElementsByType(text.P):
        # Track the list position
        i +=1
        # Extract the text
        t = teletype.extractText(element)
        # Check if each of the headers in our headers list is present within the text
        for header in headers:
            if header in t:
                # If yes, update our dictionary to record the header, and its position in the text
                header_position.update({header: i})
                # Then strip the header itself from the text, and any whitespace
                t = t.lstrip(header).strip()
        # Append the line of text to our text list
        if t != "":
            text_content.append(t)

    return text_content, header_position

def write_md(header, cont):

    headers = ["Article title:", "Authors:", "Journal:", "Date of Publication:", "URL:", "My Synopsis:", "1) What is the central argument that the authors want to make?", "2) What is the method that the authors use to make that argument?", "3) What results do the authors obtain from their method?", "4) What conclusions do the authors draw from their results?", "5) What counter-arguments, limitations, or alternative perspectives can shed light on the argument, method, results, or conclusions?", "Reflections:" ]


    os.chdir('/home/ben/Documents/MD_Test/ODT_readings')
    # Create a filename, based on the 1st line of text (should be title of journal/book)
    file_name = cont[0] + ".md"
# Create and write the new file (note this will raise file error if the file name already exists)
    try:
        with open(file_name, "x") as file:
            # Write a title header
            file.write(f"# Title: \n\n{cont[header['Article title:']]}\n\n")
            header.pop("Article title:")
            # Write the content from the title in our dictionary (Note: This will break if it is not present, but it should be in all our cases). Its also a little bit inefficient, I get an error when I add it all into the writer above (something to do with the quotes?)
            # For each of the first 4 headers in our complete potential list
            for h in headers[1:4]:
                # If it is found in the document
                if h in header:
                    # Write it as a 2nd heading along with the content of the text
                    file.write(f"## {h} \n\n{cont[header[h]]}\n\n")
                    header.pop(h)
            # If there is a URL
            if header["URL:"]:
                # Write the sub-heading, and add the link into the document
                file.write(f"## URL:\n\n[link]({cont[header['URL:']]})\n\n")
                header.pop("URL:")

        ######## Begin notes section ########
            file.write("# Notes\n\n")
            # Create a list of the present headers
            header_keys = list(header.keys())
            # For each of the present headers, excluding the last one (so we don't fall out of index range)
            # Create a header value, and its position in the list
            for position, h in enumerate(header_keys[:-1]):
                # Write the header as a 2nd header
                file.write(f"## {h}\n\n")
                # For text in the range between the header and the next header
                for text in cont[header[h]:header[header_keys[position+1]]]:
                    # Write each sentence with a double-break between
                    file.write(f"{text}\n\n")
            # Then write the final header
            file.write(f"## {header_keys[-1]}\n\n")
            # And the text associated with the final header
            for text in cont[header[header_keys[-1]]:]:
                file.write(f"{text}\n\n")
    except OSError:
        return ValueError




## Executor
if __name__ == "__main__":
    main()