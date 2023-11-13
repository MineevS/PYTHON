#  Mineev S. A. [25.10.2023]

from BSTee import BSTree


if __name__ == '__main__':
    bst1 = BSTree(2)

    bst1.insert(17)
    bst1.insert(1)
    bst1.insert(34)
    bst1.insert(3)
    bst1.insert(3)
    bst1.insert(9)
    bst1.insert(18)

    for i in bst1:
        print(i)
