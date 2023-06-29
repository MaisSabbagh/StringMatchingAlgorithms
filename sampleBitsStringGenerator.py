import random
import webbrowser


LENGTH2MB = 2100000

# generate random bit-strings samples
def generate_Bit_Strings(length):
    bits_string = ""
    for i in range(0,length):
        bits_string += str(random.randint(0,1))
    return bits_string

# create file samples
def generate_file(file_name):
    """ Tags of HTML that styles the body to wrap the words to fit it in the HTML page"""
    html_file = "<html><head><style>body {word-wrap: break-word;}</style></head><body>"
    html_file += generate_Bit_Strings(LENGTH2MB)
    html_file += "</body></html>"
    
    with open(file_name, "w") as f:
        f.write(html_file)

generate_file("C:\\Users\\LENOVO\Desktop\\Algorithms\\bitsSample1.html")
generate_file("C:\\Users\\LENOVO\Desktop\\Algorithms\\bitsSample2.html")
generate_file("C:\\Users\\LENOVO\Desktop\\Algorithms\\bitsSample3.html")
#webbrowser.open("output.html")