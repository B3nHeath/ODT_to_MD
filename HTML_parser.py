from bs4 import BeautifulSoup
import re
from statistics import mode
import sys

def main():
    # Open the file we want and save it as soup
    soup = BeautifulSoup(sys.argv[1], "html.parser")
    
    # Create an empty dictionary to store unique tags classes found in body, and later their respective attributes
    classes = dict()

    # For each css class associated with <p> or <span>
    for tag in soup.find_all(["p","span"]):
        # Add it to the dictionary
        classes[tag["class"][0]] = None

    # Update dictionary with class info
    classes = css_parser(soup, classes)

    # Obtain the modal size of font in text
    modal_font = mode_font(classes)
    # Obtain list of all the bigger fonts in text
    larger_fonts = large_fonts(classes, modal_font)
    
    # For each class name, convert the font size to body or appropriate heading level (determined by position in larger font list)
    for class_name in classes:
        # if font size is not present, or it is less than or equal to the modal font, assign it the body tag
        if "font-size" not in classes[class_name] or classes[class_name]["font-size"] <= modal_font:
            classes[class_name]["font-size"] = "body"
        # Otherwise, assign it to H# according to the font-sizes position in our larger font index (+1)
        else:
            classes[class_name]["font-size"] = "H" + str(larger_fonts.index(classes[class_name]["font-size"]) + 1)

    # Initialise empty list to store extracted text
    text_extract = text_extraction(soup.body)

    md_text = formatting(text_extract, classes)

    with open(f"/home/ben/Python/Projects/ODT_converter/New_files/{sys.argv[2]}.md", "w") as file:
        file.write(md_text)



def css_parser(soup, classes):
    # Parse out the style information from the soup
    style = str(soup.head.style)

    # For each of the classes in the dictionary
    for class_name in classes.keys():
        # Create a space to store obtained class info
        class_info = {}
        # Search for the class and save content
        m = re.search(fr"{class_name}\s*{{(.*?)}}", 
                  style, flags=re.DOTALL)
        
        # Check if there is font-size information and store it
        if fs_match := re.search(r"font-size:\s*(\d+?)pt;", m.group(1)):
            class_info["font-size"] = int(fs_match.group(1))

        # Check if there is boldness information and store it
        if fb_match := re.search(r"font-weight:\s*(\w+?);", m.group(1)):
            # If it is bold, store it in class info as true
            if fb_match.group(1) == "bold":
                class_info["boldness"] = True
        
        # If there is italic information, store it
        if fi_match := re.search(r"font-style:\s*(\w+?);", m.group(1)):
            # If it is italic, store it in class info as true
            if fi_match.group(1) == "italic":
                class_info["italicism"] = True

        # Store class info in the classes dictionary
        classes[class_name] = class_info

    return classes



def mode_font(classes):
    # Initialise a value to store overall font size
    font_sizes = []

    # for each class in the classes dictionary which has a stored font-size
    for class_name in [class_values for class_values in classes if "font-size" in classes[class_values]]:
            font_sizes.append(classes[class_name]["font-size"])

    # Return mode of font_sizes
    return mode(font_sizes)



def large_fonts(classes, mode_font):
    larger_fonts = set()

    # for each class in the classes dictionary which has a stored font-size
    for class_name in [class_values for class_values in classes if "font-size" in classes[class_values]]:
        # If the font size is bigger than the mode
        if classes[class_name]["font-size"] > mode_font:
            # add to the set
            larger_fonts.add(classes[class_name]["font-size"])

    return sorted(larger_fonts, reverse=True)


def text_extraction(text):
    # Initialise empty texts list
    texts = []
    # For all of the strings present in the body of the HTML file
    for string in text.strings:
        # Intialise empty storer of css_class
        css_classes = ""
        # If string has a parent
        if string.parent:
            # Get the CSS class of the parent element
            css_classes = ' '.join(string.parent.get("class", ""))
        # Append the string and the css class as a tuple into the texts list
        texts.append((string, css_classes))
    # Return the text
    return texts


def formatting(text_extract,classes):
    # Storage of converted text
    md_text = ""
    # Storer of previous heading level
    prv_ttl_lvl = 0

    for text, style in text_extract:
        # Double up all newline characters (looks better for markdown)
        text = text.replace("\n", "\n\n")
        # Indicator for emphasis level (number of "*" to add)
        emphasis = 0
        # Indicator for title level (number of "#" to add)
        ttl_lvl = 0
        # If there is a style attributed to this text, look through it
        if style in classes:
            # If there is boldness, add "**"
            if "boldness" in classes[style]:
                emphasis += 2
            # If there is italicism, add "*"
            if "italicism" in classes[style]:
                emphasis += 1
            # If font-size if present in class style
            if "font-size" in classes[style]:
                # find out if font-size is a heading level
                if match := re.search(r"H(\d+)", classes[style]["font-size"]):
                    # Add number of "#" according to heading level
                    ttl_lvl += int(match.group(1))

        # If current heading level is same as one before, and is a heading
        if prv_ttl_lvl == ttl_lvl and ttl_lvl > 0:
            if match := re.search(r"^(\s*)(.+?)(\s*)$", text):
                # Compile markdown text with hyphen between this and previous, don't add heading level
                text = "- " + match.group(2) + match.group(3)

        # If there is a heading level, add hashes
        elif ttl_lvl > 0:
    # Identify and split into groups. (whitespace)(any text)(whitespace)
            if match := re.search(r"^(\s*)(.+?)(\s*)$", text):
                # Compile markdown text
                text = "#"*(ttl_lvl+1) + " " + match.group(2) + match.group(3)

        # Otherwise add text
        else:
            if match := re.search(r"^(\s*)(.+?)(\s*)$", text):
                # Compile markdown text
                text = "*"*emphasis + match.group(2) + "*"*emphasis + match.group(3)

        # At end of each loop
        # Update previous title level
        prv_ttl_lvl = ttl_lvl

        # Append formatted text
        md_text += text

    # Upon completion of all loops, Return text
    return md_text




if __name__ == "__main__":
    main()
