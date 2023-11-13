# Mineev S. A. [25.10.2023]


class BSTreeNode(object):
    def __init__(self, val=None, left_node=None, right_node=None, parent=None):
        self.data = val
        self.left_node_child = left_node
        self.right_node_child = right_node
        self.parent_node = parent

    def __iter__(self):
        if self.left_node_child is not None:
            yield from self.left_node_child
        yield self.data
        if self.right_node_child is not None:
            yield from self.right_node_child

    def insert(self, val):
        if self.data is None:
            self.data = val
        elif val > self.data:
            if self.right_node_child is None:
                self.right_node_child = BSTreeNode(val)
                self.right_node_child.parent_node = self
            else:
                self.right_node_child.insert(val)
        elif val < self.data:
            if self.left_node_child is None:
                self.left_node_child = BSTreeNode(val)
                self.left_node_child.parent_node = self
            else:
                self.left_node_child.insert(val)
        else:
            pass  # Значения совпадают. Ничего не делаем.


class BSTree(object):
    def __init__(self, val=None):
        if val is None:
            self.root = None
            self.count_nodes = 0
        else:
            self.root = BSTreeNode(val)
            self.count_nodes = 1

    def __len__(self):
        return self.count_nodes

    def length(self):
        return self.__len__()

    def __iter__(self):
        return self.root.__iter__()

    def insert(self, val):
        if self.root is None:
            self.root = BSTreeNode(val)
            self.count_nodes = 1
        if self.root is not None:
            self.root.insert(val)
            self.count_nodes += 1
