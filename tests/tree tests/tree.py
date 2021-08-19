class Tree:
    master = None
    children = []
    all_children = []
    name = None
    tables = []

    def handle_branches():
        branches = Tree.__subclasses__()
        for branch in branches:
            branch.children = branch.get_children()

    @classmethod
    def get_children(self):
        children = []
        branches = Tree.__subclasses__()
        for branch in branches:
            if branch.master == self:
                children.append(branch)
        return children


class A(Tree):
    tables = [1, 2, 3]
    name = "hi"
    find_screen = True

class B(Tree):
    master = A
    tables = ["sksjsbdx"]
    name = "hdjsdjs7383j"

class C(Tree):
    master = A
    tables = ["sksjs", 8292]
    name = "hdjsdjs7djhdjkd"

class D(Tree):
    master = C
    tables = 920283930
    name = 23320

Tree.handle_branches()
