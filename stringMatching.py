import time
from timeit import default_timer as timer
import re

BITS_PATTERN_LENGTH = 20
# test = "Test.html"
bits = ""
pattern = ""


def update_sample_html(text, pattern):

    patternmatch = []  #initializes an empty list
    for k in range (len(text) - len(pattern) +1):
        if text[k:k + len(pattern)] == pattern:  #checks if the pattern exists in a specific section of the text
            patternmatch.append((pattern, k, k + len(pattern)))  #if it does match, the pattern found along with its starting
                                                                #and ending index is added to the list

    updated_string = "<style>body {word-wrap: break-word;}</style>"  
    last_end = 0

    for i in patternmatch:   
        start = i[1]                #start stores the starting index of the pattern present in tuple i of the list of tuples patternmatch
        end = i[2]          #end stores the ending index of the pattern present in tuple i of the list of tuples patternmatch 
        updated_string += text[last_end:start] + "<mark>" + i[0] + "</mark>"   # the pattern located by the indexes start and end is highlighted in the text 
        last_end = end      #sets last_end to the end index of the pattern to start looking for the next occurrence after the previous occurrence was highlighted 

    updated_string += text[last_end:]   

    with open("Updatedhtmlfile.html", "w",  encoding="utf-8") as file:  # to be able to read the html file
        file.write(updated_string)

#-----------------------------------------------------------------------------------------------------


def shift_table(p):
    bad_symbol = {}  # declare a dictionary to store the bad symbol table
    i = 0
    """ Makes all of the list shift by the length of the pattern. 
        It will be updated in the 2nd for loop """
    for i in range(len(p)):
        bad_symbol[p[i]] = len(p)
    for i in range(len(p) - 1):
        # calculate distance of every character to the end of the pattern.
        # if the key-value exists in the dictionary, the value is updated
        bad_symbol[p[i]] = len(p) - i - 1
    print("Bad-Symbol Table: ")
    # Print bad symbol table
    for key, value in bad_symbol.items():
        print(f"{key}| {value}")
    return bad_symbol

#-----------------------------------------------------------------------------------------------------

def good_suffix_table(p):
    p_length = len(p)                      
    table = [p_length] * (p_length - 1)   # Intiate an array with size of the pattern
    table_dict = {}

    for x in range(1, p_length): # outer loop for sub patterns
        subs = p[p_length - x: p_length]
        sub_len = len(subs) #check if the suffix exist in the pattern

        mc = p[p_length - x - 1: p_length - x] 

        for y in range(p_length - 2, -1, -1): # loops until end of pattern 
            check = True   

            for z in range(0, sub_len):
                if y - z < 0:
                    break
                if p[y - z] != subs[sub_len - z - 1]: 
                    check = False
                    break

            if check:  # similar to bad symbol increments shift values according to distance and placement of the character
                z += 1

                if y - z < 0:
                    table[x - 1] = p_length - y - 1
                    break
                else:
                    if p[y - z] != mc[0]:
                        table[x - 1] = p_length - y - 1
                        break

    print("Good-Suffix Table: ")
    #print good suffix table
    for key, val in enumerate(table, start=1):
        table_dict[key] = val
        print(f"{key}|{val}")

    return table_dict

#-----------------------------------------------------------------------------------------------------

def brute_force(text, pattern):
    updated_text = ""
    print("Brute Force Algorithm with Pattern " + pattern + ":")
    # start = time.time()
    start = timer()
    occurrence = 0      #keeps track of how many times each pattern occurs
    count = 0           #keeps track of whether or not all the characters in the pattern have been matched
    comparisons = 0     #keeps track of the number of comparisons done so far
    for i in range(len(text) - len(pattern) + 1):    #the outer for loop iterates through the text
        for j in range(len(pattern)):          #inner for loop iterates through pattern
            comparisons = comparisons + 1  # ------------   #counts the number of comparisons 
            if text[i + j] == pattern[j]:       #checks if the character in text matches character in pattern
                count = count + 1           
                if len(pattern) == count:       # if length of pattern and count matches (all pattern matches)
                    occurrence = occurrence + 1   
                    count = 0  # reset count
                    break
            else:
                count = 0
                break
    end = timer()    
    interval = end - start
    print("occurrence = " + str(occurrence) + ", comparisons = " + str(comparisons) + ", time = " + str(
        interval * 1000) + " ms.")
    update_sample_html(text,pattern)   #highlights the pattern in the file and creates an updated file
    occurrence = 0      #reset occurrence

 #-----------------------------------------------------------------------------------------------------   

def HorspoolMatching(text, pattern):
    print("\nHorspool's Algorithm with Pattern " + pattern + ":")
    table = shift_table(pattern)

    occurrence = 0 #keeps track of how many times each pattern occurs
    i = len(pattern) - 1  # pattern's right end position
    comparisons = 0 #keeps track of the number of comparisons done so far

    start = timer()
    while i <= len(text) - 1: # iteration through text
        matched = 0 #iterates 
        while matched <= (len(pattern) - 1) and pattern[len(pattern) - 1 - matched] == text[i - matched]:
            matched = matched + 1
            comparisons = comparisons + 1
        if matched == len(pattern):  # if the pattern matches the text
            occurrence = occurrence + 1
            i = i + table[text[i]]  # shift by the last character in the text that aligns with the pattern
        else:
            comparisons = comparisons + 1
            if text[i] not in pattern:
                i = i + len(pattern)
            else:
                i = i + table[text[i]]  # shift by the last character in the text that aligns with the pattern

    end = timer()
    interval = end - start
    print("Horspool occurrence = " + str(occurrence) + ", comparisons = " + str(comparisons) + ", time = " + str(
        interval * 1000) + " ms.")
    update_sample_html(text,pattern)

#-----------------------------------------------------------------------------------------------------



def BoyerMoore(text, pattern):
    print("\nBoyer Moore's Algorithm with Pattern " + pattern + ":")
    BStable = shift_table(pattern)
    GStable = good_suffix_table(pattern)

    occurrence = 0
    i = len(pattern) - 1   #i set to index of rightmost character in pattern
    comparisons = 0     

    start = timer()
    while i <= len(text) - 1:     #runs until i reaches end of text
        matched = 0
        while matched <= (len(pattern) - 1) and pattern[len(pattern) - 1 - matched] == text[i - matched]: # inner loop compares characters from the rightmost position of the pattern and the corresponding characters in the text.
            matched = matched + 1           #incremented as long as characters match
            comparisons = comparisons + 1    #incremented as long as characters match   
        if matched == len(pattern): # if the pattern matches the text
            occurrence = occurrence + 1     #occurrence incremented to indicate a match is found
            i = i + 1       #move to next position
        else:
            comparisons = comparisons + 1       
            if text[i] not in pattern:
                i = i + len(pattern)     #if text[i] not in pattern, entire pattern shifted by len(pattern) positions
            elif (matched == 0):
                i = i + BStable[text[i]] # shift according to bad symbol table if no matches found
            else:
                if (BStable[text[i]] > GStable[matched]):
                    i = i + (BStable[text[i]] - matched) # Shift according to Bad symbol - matched suffix
                else:
                    i = i + GStable[matched] # Shift by the mismatched character according to good suffix
            # comparisons = comparisons + 1

    end = timer()
    interval = end - start
    print("Boyer Moore's occurence = " + str(occurrence) + ", comparisons = " + str(comparisons) + ", time = " + str(
        interval * 1000) + " ms.")
    update_sample_html(text,pattern)
    print("-------------------------")

#-----------------------------------------------------------------------------------------------------
 
    
def Menu():
    print("Menu:")
    print("1. Brute Force")
    print("2. Horspool Matching")
    print("3. Boyer-Moore")
    print("4. ALL")
    print("5. Return to Previous Menu")

def get_user_choice():
    choice = input("Enter your choice (1-5): ")
    return choice

def typeMenu():
    print("Choose Type: ")
    print("1. Text")
    print("2. Bits")
    print("3. Test (Note 5)")
    print("4. Exit")

def bitsFileMenu():
    print("Choose File: ")
    print("1. bitsSample1")
    print("2. bitsSample2")
    print("3. bitsSample3")
    print("4. Return to Previous Menu")

def textFileMenu():
    print("Choose File: ")
    print("1. textSample1")
    print("2. textSample2")
    print("3. textSample3")
    print("4. Return to Previous Menu")

# Bits, Text, or neither
def get_type_choice():
    choice = input("Enter your choice (1-4): ")
    return choice

# selects which sample text to work on
def get_text_choice():
    choice = input("Enter your choice (1-4): ")
    return choice

# selects which sample bit string to work on
def get_bits_choice():
    choice = input("Enter your choice (1-4): ")
    return choice

#-----------------------------------------------------------------------------------------------------


while True:
    subPattern = ""
    text = ""
    typeMenu()
    type_choice = get_type_choice()

    if type_choice == '1':  #if file type is Text 
        while True:
            subPattern = ""
            textFileMenu()          #display options of text samples
            text_choice = get_text_choice()

            if text_choice == '1':      #sample text file is sample 1
                file = "textSample1.html"
                with open(file, "r",  encoding="utf-8") as f:       #helps read the html file as text file to avoid tags
                    text = f.read()
                pattern = "bed-clothes"  #pattern for Worst Case

                while True:
                    subPattern = ""
                    Menu()          #displays menu for algorithm types 
                    user_choice = get_user_choice()
                    print("------------------------------")

                    if user_choice == '1':      #if brute force is chosen
                        for i in pattern:
                            subPattern += i     #breaks the pattern into sub patterns 
                            brute_force(text, subPattern)

                    elif user_choice == '2':     #if horspool is chosen
                        for i in pattern:
                            subPattern += i     #breaks the pattern into sub patterns
                            HorspoolMatching(text, subPattern)

                    elif user_choice == '3':    #if boyer moore is chosen 
                        for i in pattern:
                            subPattern += i     #breaks the pattern into sub patterns 
                            BoyerMoore(text, subPattern)    

                    elif user_choice == '4':        #if all the algorithms are run 
                        brute_force(text, pattern)  
                        HorspoolMatching(text, pattern)
                        BoyerMoore(text, pattern)

                    elif user_choice == '5':        #exit
                        break

                    else:
                        print("Invalid choice. Please try again.")

            elif text_choice == '2':        #sample text file is sample 2
                file = "textSample2.html"
                
                with open(file, "r",  encoding="utf-8") as f:
                    text = f.read()
                pattern = "captain"
                while True:
                    subPattern = ""
                    Menu()
                    user_choice = get_user_choice()
                    print("------------------------------")

                    if user_choice == '1':
                        for i in pattern:
                            subPattern += i
                            brute_force(text, subPattern)

                    elif user_choice == '2':
                        for i in pattern:
                            subPattern += i
                            HorspoolMatching(text, subPattern)

                    elif user_choice == '3':
                        for i in pattern:
                            subPattern += i
                            BoyerMoore(text, subPattern)

                    elif user_choice == '4':
                        brute_force(text, pattern)
                        HorspoolMatching(text, pattern)
                        BoyerMoore(text, pattern)

                    elif user_choice == '5':
                        break

                    else:
                        print("Invalid choice. Please try again. 289")

            elif text_choice == '3':                #sample text file is sample 3
                file = "textSample3.html"       
                with open(file, "r",  encoding="utf-8") as f:
                    text = f.read()
                pattern = "DIPLOBLASTIC"
                while True:
                    subPattern = ""
                    Menu()
                    user_choice = get_user_choice()
                    print("------------------------------")

                    if user_choice == '1':
                        for i in pattern:
                            subPattern += i
                            brute_force(text, subPattern)

                    elif user_choice == '2':
                        for i in pattern:
                            subPattern += i
                            HorspoolMatching(text, subPattern)

                    elif user_choice == '3':
                        for i in pattern:
                            subPattern += i
                            BoyerMoore(text, subPattern)

                    elif user_choice == '4':
                        brute_force(text, pattern)
                        HorspoolMatching(text, pattern)
                        BoyerMoore(text, pattern)

                    elif user_choice == '5':
                        break

                    else:
                        print("Invalid choice. Please try again. 323")

            elif text_choice == '4':
                break

            else:
                print("Invalid choice. Please try again. 329")

    # if bits file is chosen
    elif type_choice == '2':
        while True:
            subPattern = ""
            bitsFileMenu()
            bits_choice = get_bits_choice()

            if bits_choice == '1':              #bit sample chosen is sample 1 
                file = "bitsSample1.html"
                with open(file, "r") as f:
                    bits = f.read()

                # Remove style tag
                text = re.sub(r'<style.*?>.*?</style>', '', bits, flags=re.DOTALL)      

                # remove remaining tags
                text = re.sub(r'<[^>]+>', '', text)

                # Pattern will be the first 20 charcaters
                pattern = text[:BITS_PATTERN_LENGTH]
                while True:
                    subPattern = ""
                    Menu()
                    user_choice = get_user_choice()
                    print("------------------------------")

                    if user_choice == '1':      
                        for i in pattern:
                            subPattern += i
                            brute_force(text, subPattern)

                    elif user_choice == '2':
                        for i in pattern:
                            subPattern += i
                            HorspoolMatching(text, subPattern)

                    elif user_choice == '3':
                        for i in pattern:
                            subPattern += i
                            BoyerMoore(text, subPattern)

                    elif user_choice == '4':
                        brute_force(text, pattern)
                        HorspoolMatching(text, pattern)
                        BoyerMoore(text, pattern)

                    elif user_choice == '5':
                        break

                    else:
                        print("Invalid choice. Please try again. 379")

            # Average case with Sample 2
            elif bits_choice == '2':
                file = "bitsSample2.html"
                with open(file, "r") as f:
                    bits = f.read()

                # Remove style tag
                text = re.sub(r'<style.*?>.*?</style>', '', bits, flags=re.DOTALL)

                # remove remaining tags
                text = re.sub(r'<[^>]+>', '', text)

                # Pattern will be selected from the middle of the string
                # Use // for integer division
                pattern = "00111111101110101110"

                while True:
                    subPattern = ""
                    Menu()
                    user_choice = get_user_choice()
                    print("------------------------------")

                    if user_choice == '1':
                        for i in pattern:
                            subPattern += i
                            brute_force(text, subPattern)

                    elif user_choice == '2':
                        for i in pattern:
                            subPattern += i
                            HorspoolMatching(text, subPattern)

                    elif user_choice == '3':
                        for i in pattern:
                            subPattern += i
                            BoyerMoore(text, subPattern)

                    elif user_choice == '4':
                        brute_force(text, pattern)
                        HorspoolMatching(text, pattern)
                        BoyerMoore(text, pattern)

                    elif user_choice == '5':
                        break

                    else:
                        print("Invalid choice. Please try again. 424")

            elif bits_choice == '3':
                file = "bitsSample3.html"
                with open(file, "r") as f:
                    bits = f.read()

                # Remove style tag
                text = re.sub(r'<style.*?>.*?</style>', '', bits, flags=re.DOTALL)

                # remove remaining tags
                text = re.sub(r'<[^>]+>', '', text)

                pattern = text[len(text) - BITS_PATTERN_LENGTH:]  # worst case

                while True:
                    subPattern = ""
                    Menu()
                    user_choice = get_user_choice()
                    print("------------------------------")

                    if user_choice == '1':
                        for i in pattern:
                            subPattern += i
                            brute_force(text, subPattern)

                    elif user_choice == '2':
                        for i in pattern:
                            subPattern += i
                            HorspoolMatching(text, subPattern)

                    elif user_choice == '3':
                        for i in pattern:
                            subPattern += i
                            BoyerMoore(text, subPattern)

                    elif user_choice == '4':
                        brute_force(text, pattern)
                        HorspoolMatching(text, pattern)
                        BoyerMoore(text, pattern)

                    elif user_choice == '5':
                        break

                    else:
                        print("Invalid choice. Please try again. 468")

            elif bits_choice == '4':
                break

            else:
                print("Invalid choice. Please try again. 474")
    #test case
    elif type_choice == '3':
        pattern = "AT_THAT"
        file = "Test.html"
        with open(file, "r") as f:
            bits = f.read()
        # Remove style tag
        text = re.sub(r'<style.*?>.*?</style>', '', bits, flags=re.DOTALL)

        # remove remaining tags
        text = re.sub(r'<[^>]+>', '', text)
            
        brute_force(text, pattern)
        HorspoolMatching(text, pattern)
        BoyerMoore(text, pattern)    
            
    
    elif type_choice == '4':
        break

    else:
        print("Invalid choice. Please try again.480")
