from bplustree_with_visualizer import GraphableBPlusTree
import os
from mathml_extractor import operator_extractor, operand_extractor
import pickle
from B_Tree import BTree


dataset_path = "./../../Downloads/dataset_full/dataset_full/math/"


def bplustree_builder():
    '''
    This method must be run first on any new machine in order to create and pickle the b+ tree.
    For it to function properly, please change the dataset_path variable above to the location of the math folder within the dataset on your machine.
    '''
    bplustree = GraphableBPlusTree(order=3)
    all_the_folders = os.listdir(dataset_path)

    for folder in all_the_folders:
        if ".DS_Store" not in folder:
            question_path = f"{dataset_path}{folder}/question/"
            answer_path = f"{dataset_path}{folder}/answers/"
            for file in os.listdir(question_path):
                whole_path = question_path + file
                num_operands = operand_extractor(whole_path)
                indexes = operator_extractor(whole_path)
                for index in indexes:
                    bplustree.insert(index, (whole_path, num_operands))
            for file in os.listdir(answer_path):
                whole_path = answer_path + file
                num_operands = operand_extractor(whole_path)
                indexes = operator_extractor(whole_path)
                for index in indexes:
                    bplustree.insert(index, (whole_path, num_operands))

    with open('./pickled_tree.txt', 'wb') as file:
        pickle.dump(bplustree, file)
    # bplustree.show_all_data()

def btree_builder():
    btree = BTree(3)

    all_the_folders = os.listdir(dataset_path)

    for folder in all_the_folders:
        if ".DS_Store" not in folder:
            question_path = f"{dataset_path}{folder}/question/"
            answer_path = f"{dataset_path}{folder}/answers/"
            for file in os.listdir(question_path):
                whole_path = question_path + file
                num_operands = operand_extractor(whole_path)
                indexes = operator_extractor(whole_path)
                for index in set(indexes):
                    btree.insert(index, (whole_path, num_operands))
            for file in os.listdir(answer_path):
                whole_path = answer_path + file
                num_operands = operand_extractor(whole_path)
                indexes = operator_extractor(whole_path)
                for index in set(indexes):
                    btree.insert(index, (whole_path, num_operands))

    # btree.printTree(btree.root)

    with open('./pickled_b_tree.txt', 'wb') as file:
        pickle.dump(btree, file)


def tester_tree():
    '''
    This method can be modified and used to create a smaller tree with speficied data for testing.
    Here, the sample data is specified as "test2.xml" and "test3.xml" amd the tree is stored as "tester_tree.txt".
    '''
    bplustree = GraphableBPlusTree(order=3)
    for file in ["./test2.xml", "./test3.xml"]:
        num_operands = operand_extractor(file)
        indexes = operator_extractor(file)
        for index in indexes:
            bplustree.insert(index, (file, num_operands))
    with open('./tester_tree.txt', 'wb') as file:
        pickle.dump(bplustree, file)
    bplustree.show_all_data()

if __name__ == "__main__":
    # bplustree_builder()
    # tester_tree()
    btree_builder()
