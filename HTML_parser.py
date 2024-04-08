from bs4 import BeautifulSoup
import re
from statistics import mode

def main():
    # Open the file we want and save it as soup
    with open("html.txt", "r") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    # Create an empty dictionary to store unique tags classes found in body, and later their respective attributes
    classes = dict()

    for tag in soup.find_all(["p","span"]):
        # Add it to the set
        classes[tag["class"][0]] = None

    # Update dictionary with class info
    classes = css_parser(soup, classes)

    # Obtain the modal size of font in text
    modal_font = mode_font(classes)
    # Obtain list of all the bigger fonts in text
    larger_fonts = large_fonts(classes, modal_font)
    
    # For each class name, convert the font size to body or appropriate heading level (determined by position in larger font list)
    for class_name in classes:
        if "font-size" not in classes[class_name] or classes[class_name]["font-size"] <= modal_font:
            classes[class_name]["font-size"] = "body"
        else:
            classes[class_name]["font-size"] = "H" + str(larger_fonts.index(classes[class_name]["font-size"]) + 1)




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


if __name__ == "__main__":
    main()
