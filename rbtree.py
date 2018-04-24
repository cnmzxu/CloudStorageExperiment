import random

class treenode:
    def __init__(self, color, value, left, right, parent, key):
    # a node of a rbtree is a 5-list [color(0), key(1), leftson(2), rightson(3), parent(4)]
    # color: 0 is black, 1 is red
        self.color = color
        self.value = value
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent
        self.minkey = key
        self.maxkey = key

    def __str__(self):
        return str([self.key, self.value])

class rbtree:
    def __init__(self, key = lambda x:x):
        self.nil = treenode(0, -1, None, None, None, -1)
        self.nil.left = self.nil.right = self.nil.parent = self.nil
        self.root = self.nil
        self.key = key
        self.size = 0

    def __left_rotate__(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
            x.maxkey = y.left.maxkey
        else:
            x.maxkey = x.key
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        y.minkey = x.minkey
        x.parent = y

    def __right_rotate__(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y
            y.minkey = x.right.minkey
        else:
            y.minkey = y.key
        x.parent = y.parent
        if y.parent == self.nil:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        x.maxkey = y.maxkey
        y.parent = x

    def __insert_fixup__(self, z):
        while z.parent.color == 1:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 1:
                    z.parent.color = 0
                    y.color = 0
                    z.parent.parent.color = 1
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.__left_rotate__(z)
                    z.parent.color = 0
                    z.parent.parent.color = 1
                    self.__right_rotate__(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == 1:
                    z.parent.color = 0
                    y.color = 0
                    z.parent.parent.color = 1
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.__right_rotate__(z)
                    z.parent.color = 0
                    z.parent.parent.color = 1
                    self.__left_rotate__(z.parent.parent)
        self.root.color = 0

    def __insert(self, z):
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.minkey < x.minkey:
                x.minkey = z.minkey
            if z.maxkey > x.maxkey:
                x.maxkey = z.maxkey
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.color = 1
        self.__insert_fixup__(z)

    def insert(self, value):
        self.__insert(treenode(None, value, None, None, None, self.key(value)))
        self.size += 1

    def __find_near(self, node, key, sigma):
        if key + sigma < node.minkey or key - sigma > node.maxkey:
            return tuple()
        if key + sigma < node.key:
            return self.__find_near(node.left, key, sigma)
        if key + sigma >= node.key and key - sigma <= node.key:
            return self.__find_near(node.left, key, sigma) +  (node.value, ) + self.__find_near(node.right, key, sigma)
        if key - sigma > node.key:
            return self.__find_near(node.right, key, sigma)

    def find_near(self, key, sigma):
        return self.__find_near(self.root, key, sigma)

    def __len__(self):
        return self.size
    
    def __print__(self, node, ind):
        if node != self.nil:
            print(' ' * ind, node)
            self.__print__(node.left, ind + 1)
            self.__print__(node.right, ind + 1)
    
    def __str__(self):
        self.__print__(self.root, 0)
        return ''

def test():
    t = rbtree(lambda x:x)
    for i in range(100):
        t.insert(random.randint(0, 10000))
    t.insert(4000)
    #print(t)
    print(t.find_near(4000, 0))

#test()