from xml.etree import ElementTree
import os
from collections import Counter

def make_tree(filename: str):
    '''
    Given the name of a MathML file, make_tree() parses the XML and returns the root of the ElementTree.
    If the file cannot be parsed, returns None.
    '''
    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()
    except: #The '&' character causes the xml to be malformed. This except block handles replacing '&' with its escape.
        with open(filename, 'r') as malformed:
            text = malformed.read()
            if '&' in text:
                text = text.replace('&', '&amp;')
        try:
            root = ElementTree.fromstring(text)
        except:
            print(f"MALFORMED MATHML: {filename}")
            return None
    return root

def operator_extractor(filename: str):
    '''
    Given the name of a MathML file, operator_extractor() returns a list of the encodings of all the operators in that formula.
    If the file cannot be parsed, returns an empty list.
    '''
    ns = "{http://www.w3.org/1998/Math/MathML}" # MathML namespace
    root = make_tree(filename)
    keywords = []
    if not root:
        return keywords
    
    for node in root.findall(f'.//'): # This findall() will return every node under the root node in depth-first order.
        if node.tag == ns + 'mo' and node.text: # Operator tag
            op = node.text.strip()

            if op.isalpha():
                keywords.append(op)
            else:
                try:
                    keywords.append(format(ord(op), '04X')) # ord() converts a character to its unicode encoding. i converted this to 4 digits of hex.
                except TypeError: # A string with more than one character is the operator
                    if op.startswith('&#x'): # This condition handles the case where the encoding for the operator is given, rather than the literal character.
                        index = op[4:-1]
                        keywords.append(index)
                    else:
                        keywords.append(op)
                
        elif node.tag == ns + 'msqrt':
            keywords.append('221A') # Encoding for square root character, since the literal character does not usually appear in MathML.
        
    return keywords

def operand_extractor(filename: str):
    '''
    Given the name of a MathML file, operand_extractor() returns the number of identifiers and numbers in the formula.
    If the file cannot be parsed, returns 0.
    '''
    ns = "{http://www.w3.org/1998/Math/MathML}" # MathML namespace
    root = make_tree(filename)
    if not root:
        return 0
    
    numbers = root.findall(f".//{ns}mn")
    identifiers = root.findall(f".//{ns}mi")
    return len(numbers) + len(identifiers)

def get_dominant_operator(filename: str):
    '''
    Given a MathML file, generates the dominant operator for index in clustering and secondary approach.
    Returns the most frequent operator or, if multiple operators with the highest frequency, returns first in the file.
    If no operators in the formula, returns None.
    '''
    operators = operator_extractor(filename)
    if operators:
        counts = Counter(operators)
        max_count = max(counts.values())
        most_frequent = [operator for operator, freq in counts.items() if freq == max_count]
        return most_frequent[0]
    return None

if __name__ == "__main__":
    all_the_folders = os.listdir('./../../Downloads/dataset_full/dataset_full/math/') #may need to change path depending on where the dataset is stored on your machine
    for folder in all_the_folders:
        if ".DS_Store" not in folder:
            path = f'./../../Downloads/dataset_full/dataset_full/math/{folder}/question/' #change question to answers to go through answer files
            for file in os.listdir(path):
                indexes = operator_extractor(path + file)
                