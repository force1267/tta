red = True
black = False
class node:
    def __init__(self, val):
        self.val = val
        self.l = self.r = self.p = None
        self.color = red
    def print(self, index, level = 0):
        print("\t" * level, self.val[index])
        if self.r is not None:
            self.r.print(index, level + 1)
        else:
            print("\t" * (level + 1), "---")
        if self.l is not None:
            self.l.print(index, level + 1)
        else:
            print("\t" * (level + 1), "---")
    def printrb(self, level = 0):
        print("\t" * level, "red" if self.color else "black")
        if self.r is not None:
            self.r.printrb(level + 1)
        else:
            print("\t" * (level + 1), "black")
        if self.l is not None:
            self.l.printrb(level + 1)
        else:
            print("\t" * (level + 1), "black")
class rbt:
    def __init__(self, index):
        self.index = index
        self.root = None
    def __rotate(self, n, right = True):
        if n is None:
            return
        root = n
        rootp = root.p
        pivot = root.l if right else root.r
        if right:
            root.l = pivot.r
            if pivot.r is not None:
                pivot.r.p = root
            pivot.r = root
        else:
            root.r = pivot.l
            if pivot.l is not None:
                pivot.l.p = root
            pivot.l = root
        pivot.p = root.p
        root.p = pivot
    def __gc(self, n): # get color
        return black if n is None else n.color
    def __recolor(self, n):
        if self.__gc(n.p) == black:
            return
        left = n is n.p.l
        uncle = n.p.r if left else n.p.l
        n.p.color = black
        n.p.p.color = red
        if self.__gc(uncle) == red:
            uncle.color = black
            self.__recolor(n.p.p)
        else:
            self.__rotate(n.p.p, left)
    def add(self, val):
        n = node(val)
        if self.root is not None:
            now = self.root
            while True:
                left = val[self.index] <= now.val[self.index]
                if now.l is not None if left else now.r is not None:
                    now = now.l if left else now.r
                else:
                    n.p = now
                    if left:
                        now.l = n
                        break
                    else:
                        now.r = n
                        break
            # fix color
        else:
            self.root = n
            n.color = black
    def find(self, q):
        now = self.root
        while now is not None:
            if q == now.val[self.index]:
                return now.val
            now = now.l if q < now.val[self.index] else now.r
        return None


if __name__ == "__main__":
    ss = [
        { "id": 951, "name": "mohammad Javad", "lastname": "asadi" },
        { "id": 952, "name": "mojtaba", "lastname": "qoli zade" },
        { "id": 953, "name": "rasam", "lastname": "moqadam" },
        { "id": 954, "name": "erfan", "lastname": "arefi" },
        { "id": 955, "name": "maniya", "lastname": "baqeri" },
        { "id": 956, "name": "fazele", "lastname": "mirpour" },
        { "id": 957, "name": "kimia", "lastname": "nemati" }
    ]
    tree = rbt("lastname")
    for s in ss:
        tree.add(s)
    tree.root.printrb()
    tree.root.print("lastname")
    while True:
        print(">{}".format(tree.find(input(">>>"))))