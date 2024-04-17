# ODT to Markdown

This project converts files within folders that are ODT files, into a markdown format. The conversion from HTML to Markdown uses python, with a bash script to go through the folder and convert files from ODT to HTML, with an option to operate it recursively. This is quite a specific project, I have been using Obsidian for a lot of my note taking, and I wanted to push my old notes into markdown format. As such, some of the choices I have made are quite spceific to my obsidian format and note-taking style (e.g. doubling new lines, starting heading levels as level 2). 

I decided to convert first to HTML with odf2xhtml and then use the HTML output to convert to Markdown. There is a module that extracts odt content in Python directly: https://pypi.org/project/odfpy/. However, I personally struggled with the documentation for this, particularly with extracting the style settings associated with text. Along with this package came the odf2xhtml package, which I used in combination with beautifulsoup: https://pypi.org/project/beautifulsoup4/

# Using this project

This project is quite specific to me, but should be able to be used with a minimal amount of changes. In particular, changes within the Python script. Firstly, the designated file to send the markdown files to should be changed to wherever the user would like them sent. Some other features of the program:

- If two sections of text have the same heading level, they are combined with a "-", rather than producing two heading levels
- All headings start at level 2 "##". This is a personal preference, since on Obsidian my heading level 1 is very prominent, which led to some presentational issues
- All newlines are doubled within my text in order to increase spacing, but this might not fit with some peoples note taking preferences
- I have yet to implement handling of lists, though this is very much an intention

### Basic rundown of project functionality:

#### Bash script:

1. Takes in name of folder we want to convert, and whether we want to handle it recurisvely
2. Goes through each file in the folder, and uses odf2xhtml to produce a HTML output
3. calls HTML_parser.py, along with the HTML output and the filename (excluding the extention)

#### Python script:

1. Creates soup object from the HTML input
2. Creates a dictionary of all the used css classes ("p" or "span") within the document
3. Extracts information about font-size, boldness, italicism associated with each class, and creates a dictionary within the dictionary to store these values
4. Identify the most common font-szie within the document
5. Create a list of all the unique font sizes bigger than the mode, in reverse order
   - Assign these fonts as heading levels, starting from "H2"
6. Collect the text from the HTML body, and format it in markdown format
7. Write the new file into a specific folder, with filename same as original ODT filename

