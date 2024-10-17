from xml.etree import ElementTree
import re
from collections import Counter
import os

def make_tree(filename: str):
    '''
    Given the name of a MathML file, make_tree() parses the XML and returns the root of the ElementTree.
    If the file cannot be parsed, returns None.
    '''
    try:
        tree = ElementTree.parse(filename)
        root = tree.getroot()
    except: #The '&' character causes the xml to be malformed. This except block handles replacing '&' with its escape.
        with open(filename, 'r', encoding="utf8") as malformed:
            text = malformed.read()
            text = text.replace('&', '&amp;')
            text = text.replace('"', '&quot;')
            text = text.replace("'", '&apos;')
            text = text.replace('><<', '>&lt;<')
            text = text.replace('>><', '>&gt;<')
        try:
            root = ElementTree.fromstring(text)
        except:
            # print(f"MALFORMED MATHML: {filename}")
            return None
    return root

def operator_extractor(filename: str, ns="{http://www.w3.org/1998/Math/MathML}"):
    '''
    Given the name of a MathML file, operator_extractor() returns a list of the encodings of all the operators in that formula.
    If the file cannot be parsed, returns an empty list.
    '''
    root = make_tree(filename)
    keywords = []
    if root is None:
        return keywords
    
    for node in root.findall(f'.//'): # This findall() will return every node under the root node in depth-first order.
        if node.tag == ns + 'mo' and node.text: # Operator tag
            op = node.text.strip()

            if bool(re.match(r"^[A-Za-z ]+$", op)):
                keywords.append(op)
            else:
                try:
                    keywords.append(format(ord(op), '04X')) # ord() converts a character to its unicode encoding. i converted this to 4 digits of hex.
                except TypeError: # A string with more than one character is the operator
                    if op.startswith('&#x'): # This condition handles the case where the encoding for the operator is given, rather than the literal character.
                        index = op[4:-1]
                        keywords.append(index)
                    else:
                        encoding = ""
                        for char in op:
                            if bool(re.match(r"[A-Za-z0-9]", char)):
                                encoding += char
                            else:
                                encoding += format(ord(char), '04X') + "_"
                        keywords.append(encoding)
                
        elif node.tag == ns + 'msqrt':
            keywords.append('221A') # Encoding for square root character, since the literal character does not usually appear in MathML.

    # it's a little sketchy, but in this block we assume the hyphen-minus (-) to be equivalent to the minus sign (−), and swith the encoding to such.
    for i, op in enumerate(keywords):
        if op == '002D':
            keywords[i] = '2212'
        
    return keywords

def operand_extractor(filename: str, ns="{http://www.w3.org/1998/Math/MathML}",version=1):
    '''
    Given the name of a MathML file, operand_extractor() returns the number of identifiers and numbers in the formula.
    If the file cannot be parsed, returns 0.
    version=1 : returns one number representing numbers + identifiers
    version=2 : returns the tuple (numbers, identifiers)
    version=3 : same as version 2, but considers any msub nodes as one identifier only
    '''
    root = make_tree(filename)
    if root is None:
        return 0, 0
    
    numbers = len(root.findall(f".//{ns}mn"))
    identifiers = len(root.findall(f".//{ns}mi"))
    if version == 3:
        for sub in root.findall(f".//{ns}msub"):
            idens = sub.findall(f".//{ns}mi")
            nums = sub.findall(f".//{ns}mn")
            counter += 1
            numbers -= len(nums)
            identifiers -= len(idens)
            identifiers += 1
    
    if version == 1:
        return numbers + identifiers
    return numbers, identifiers


def get_dominant_operator(filename: str, ns="{http://www.w3.org/1998/Math/MathML}"):
    '''
    Given a MathML file, generates the dominant operator for index in clustering and secondary approach.
    Returns the most frequent operator or, if multiple operators with the highest frequency, returns first in the file.
    If no operators in the formula, returns None.
    '''
    operators = operator_extractor(filename, ns)
    if operators:
        counts = Counter(operators)
        max_count = max(counts.values())
        most_frequent = [operator for operator, freq in counts.items() if freq == max_count]
        return most_frequent[0]
    return None

if __name__ == "__main__":
    ops = set()
    ntcir_path = "./../../Downloads/NTCIR-12_Data/MathArticles/"
    folders = os.listdir(ntcir_path)
    for folder in folders:
        articles = os.listdir(f"{ntcir_path}{folder}")
        for article in articles:
            path_to_article = f"{ntcir_path}{folder}/{article}/"
            for file in os.listdir(path_to_article):
                whole_path = path_to_article + file
                indexes = operator_extractor(whole_path, "")
                for idx in indexes:
                    ops.add(idx)
    
    print(ops)
    
                