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
        idens = 0
        nums = 0
        for sub in root.findall(f".//{ns}msub"):
            idens += len(sub.findall(f".//{ns}mi"))
            nums += len(sub.findall(f".//{ns}mn"))
            identifiers += 1
        # should subsup and mmultiscripts be included?
        identifiers -= idens
        numbers -= nums

    if version == 1:
        return numbers + identifiers
    return numbers, identifiers

def structure_scores(filename, ns="{http://www.w3.org/1998/Math/MathML}"):
    root = make_tree(filename)
    if root is None:
        return 0,0,0,0,0,0,0
    # 1) Above & 5) Below
    above = 0
    below = 0
    for frac in root.findall(f".//{ns}mfrac"):
        numerator, denominator = frac.findall("*")
        num_elems = len(numerator.findall(".//"))
        den_elems = len(denominator.findall(".//"))
        above += 1 if num_elems == 0 else num_elems
        below += 1 if den_elems == 0 else den_elems

    for underover in root.findall(f".//{ns}munderover"):
        base, under, over = underover.findall("*")
        under_elems = len(under.findall(".//"))
        over_elems = len(over.findall(".//"))
        above += over_elems if over_elems != 0 else 1 if over.tag != f"{ns}mrow" else 0
        below += under_elems if under_elems != 0 else 1 if under.tag != f"{ns}mrow" else 0
    
    for over_node in root.findall(f".//{ns}mover"):
        base, over = over_node.findall("*")
        over_elems = len(over.findall(".//"))
        above += over_elems if over_elems != 0 else 1

    for under_node in root.findall(f".//{ns}munder"):
        base, under = under_node.findall("*")
        under_elems = len(under.findall(".//"))
        below += under_elems if under_elems != 0 else 1

    # 6) Contains
    contains = 0
    for sqrt in root.findall(f".//{ns}msqrt"):
        contains += len(sqrt.findall(".//"))
    
    # 7) Left-superscript
    left_superscript = 0
    for root_node in root.findall(f".//{ns}mroot"):
        base, index = root_node.findall("*")
        base_elems = len(base.findall(".//"))
        index_elems = len(index.findall(".//"))
        contains += base_elems if base_elems > 0 else 1
        left_superscript += index_elems if index_elems > 0 else 1

    # 2) Superscript & 4) Subscript
    superscript = 0
    subscript = 0
    for subsup in root.findall(f".//{ns}msubsup"):
        base, sub, sup = subsup.findall("*")
        sub_elems = len(sub.findall(".//"))
        sup_elems = len(sup.findall(".//"))
        superscript += sup_elems if sup_elems > 0 else 1
        subscript += sub_elems if sub_elems > 0 else 1
    
    for sup_node in root.findall(f".//{ns}msup"):
        base, sup = sup_node.findall("*")
        sup_elems = len(sup.findall(".//"))
        superscript += sup_elems if sup_elems > 0 else 1
    
    for sub_node in root.findall(f".//{ns}msub"):
        base, sub = sub_node.findall("*")
        sub_elems = len(sub.findall(".//"))
        subscript += sub_elems if sub_elems > 0 else 1

    # 8) Left-subscript
    left_subscript = 0

    for multiscripts in root.findall(f".//{ns}mmultiscripts"):
        pre_flag = False
        sub_flag = True
        base = True
        for script in multiscripts.findall("*"):
            if base:
                base = False
                continue
            if script.tag == f"{ns}mprescripts":
                pre_flag = True
                sub_flag = True
                continue
            script_elems = len(script.findall(".//"))
            script_elems = script_elems if script_elems > 0 else 1 if script.tag != f"{ns}mrow" else 0
            if sub_flag:
                if pre_flag:
                    left_subscript += script_elems
                else:
                    subscript += script_elems
            else:
                if pre_flag:
                    left_superscript += script_elems
                else:
                    superscript += script_elems
            sub_flag = not sub_flag
    
    return above, superscript, subscript, below, contains, left_superscript, left_subscript


def tag_finder(filename, tag, ns="{http://www.w3.org/1998/Math/MathML}"):
    root = make_tree(filename)
    if root is None:
        return 0
    
    return len(root.findall(f".//{ns}{tag}"))


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
    others = {}
    ntcir_path = "./../../Downloads/NTCIR-12_Data/MathArticles/"
    folders = os.listdir(ntcir_path)
    for folder in folders:
        articles = os.listdir(f"{ntcir_path}{folder}")
        for article in articles:
            path_to_article = f"{ntcir_path}{folder}/{article}/"
            for file in os.listdir(path_to_article):
                whole_path = path_to_article + file
                root = make_tree(path_to_article+file)
                if root is not None:
                    for subsup in root.findall(".//msubsup"):
                        first_child = subsup.findall("*")[0]
                        if first_child.tag == "mover":
                            iden = first_child.findall("*")[0]
                            if not iden.tag in others.keys():
                                others[iden.tag] = []
                            others[iden.tag].append(path_to_article+file)

    for tag in others:
        print(f"{tag} ({len(others[tag])}): {others[tag][:5]}")
    
    # file = "./../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Discriminant/18.xml"
    # operand_extractor(file,"",3)


    '''
    mo (11692): './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/3-sphere/39.xml', 
                './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Absolute_convergence/0.xml', 
                './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Absolute_convergence/1.xml', 
                './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Absolute_convergence/19.xml', 
                './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Absolute_convergence/21.xml'
        def don't want to include. integrals and summations and such

    mrow (1107): './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Absolute_convergence/31.xml', 
                 './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Ascorbic_acid/0.xml', 
                 './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Borel-Cantelli_lemma/42.xml', 
                 './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Borel-Cantelli_lemma/48.xml', 
                 './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Borel-Cantelli_lemma/52.xml'
        seems to handle complicated terms. i fear that including this would lose some detail needed for indentifying these files

    mpadded (181): './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Actinium/6.xml', 
                   './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Americium/0.xml'
        these examples are chemistry. the padded tags are around arrows, which are operators and shouldn't be counted.
        look more into? like maybe check if there are idens or numbers inside

    mover (1129): './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Allan_variance/17.xml', 
                  './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/De_Broglie-Bohm_theory/11.xml'
                  './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Dimensionless_quantity/14.xml'
        hm. i think we should probably include this since it is mostly used adding bars above idens
        see if any other uses?

    merror (27): './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Bijection/1.xml', 
                 './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Utility/6.xml', 
                 './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Utility/7.xml', 
                 './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Utility/8.xml', 
                 './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000003/Airy_disk/38.xml'
        i don't even know man

    mtext (123): './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Body_mass_index/0.xml'
                 './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Figured_bass/6.xml', 
                 './../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/Oxidative_phosphorylation/7.xml'
        should text be considered as idens?
        it's probs more of a case by case thing.......
        MUSICAL NOTATION????????
    
    '''