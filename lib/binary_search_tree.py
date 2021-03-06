from pdb import set_trace as bp
import sys
sys.path.append('/Users/danielshin/Documents/turing/other/python/date_night_python/lib')
import node as n
import csv

class BinarySearchTree:
    def __init__(self, root=None, sorted=[]):
        self.root = root
        self.health = []

    def insert_node(self, score, movie, current_node=None, depth=1):
        if current_node is None:
            current_node = self.root

        if self.root is None:
            self.root = n.Node(score, movie)
            return 0
        else:
            if score == current_node.score():
                return None

            if score < current_node.score():
                self.insert_side("left", current_node, score, movie, depth)
            else:
                self.insert_side("right", current_node, score, movie, depth)

    def insert_side(self, side, current_node, score, movie, depth):
        if side == "left":
            if current_node.left is None:
                current_node.left = n.Node(score, movie)
                return depth
            else:
                self.insert_node(score, movie, current_node.left, depth + 1)
        else:
            if current_node.right is None:
                current_node.right = n.Node(score, movie)
                return depth
            else:
                self.insert_node(score, movie, current_node.right, depth + 1)

    def include(self, score, current_node=None, first_run=True):
        if first_run:
            current_node = self.root

        if current_node is None:
            return False
        else:
            if score == current_node.score():
                return True
            elif score < current_node.score():
                return self.include(score, current_node.left, False)
            else:
                return self.include(score, current_node.right, False)

    def depth_of(self, score, current_node=None, depth=0, first_run=True):
        if first_run:
            current_node = self.root

        if current_node is None:
            return None
        else:
            if score == current_node.score():
                return depth
            elif score < current_node.score():
                return self.depth_of(score, current_node.left, depth + 1, False)
            elif score > current_node.score():
                return self.depth_of(score, current_node.right, depth + 1, False)

    def max(self, current_node=None, first_run=True):
        if first_run:
            current_node = self.root

        if current_node.right is None:
            return current_node.data
        else:
            return self.max(current_node.right, False)

    def min(self, current_node=None, first_run=True):
        if first_run:
            current_node = self.root

        if current_node.left is None:
            return current_node.data
        else:
            return self.min(current_node.left, False)

    def sort(self, current_node=None, first_run=True):
        sorted = []

        if first_run:
            current_node = self.root

        if self.root is None:
            return sorted

        self.traverse_sort(current_node, sorted)
        return sorted

    def traverse_sort(self, node, sorted):
        if node is None:
            return

        self.traverse_sort(node.left, sorted)
        sorted.append(node.data)
        self.traverse_sort(node.right, sorted)

    def load(self, filename):
        with open(filename, 'r') as inputfile:
            for row in csv.reader(inputfile):
                self.insert_node(int(row[0]), ''.join(row[1:]).strip())

    def get_health(self, input_depth, current_node=None, current_depth=0, first_run=True):
        group_count = None

        if first_run:
            current_node = self.root
            self.health = []

        if current_node is None:
            return

        if current_depth == input_depth:
            group_count = self.node_count(current_node)
            self.health.append([current_node.score(), group_count, 100 * group_count / len(self.sort())])
            return self.health
        else:
            self.get_health(input_depth, current_node.left, current_depth + 1, False)
            self.get_health(input_depth, current_node.right, current_depth + 1, False)
            return self.health

    def node_count(self, current_node, first_run=True):
        if first_run:
            self.group_count = 0

        self.group_count += 1

        if current_node is None:
            return

        if current_node.left is not None:
            self.node_count(current_node.left, False)

        if current_node.right is not None:
            self.node_count(current_node.right, False)

        return self.group_count
