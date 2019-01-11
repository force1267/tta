red = True
black = False
class node:
    def __init__(self, val):
        self.val = val
        self.l = self.r = self.p = None
        self.color = red
    def gd(self):
        dl = self.l.gd() if self.l is not None else 0
        dr = self.r.gd() if self.r is not None else 0
        return max(dl, dr) + 1
    def printnew(self, idx):
        lines = [] # list of listes of string

        level = [] # list of nodes
        next = [] # list of nodes

        level.append(self)
        nn = 1

        widest = 0

        while nn != 0:
            line = [] # list of string

            nn = 0

            for n in level:
                if n is None:
                    line.append(None)

                    next.append(None)
                    next.append(None)
                else:
                    aa = n.val[idx]
                    line.append(aa)
                    if len(aa) > widest:
                        widest = len(aa)

                    next.append(n.l)
                    next.append(n.r)

                    if n.l != None:
                        nn = nn + 1
                    if n.r != None:
                        nn = nn + 1
            if widest % 2 == 1:
                widest = widest + 1

            lines.append(line)

            tmp = level
            level = next
            next = tmp
            next = []

        soprint = ""
        perpiece = len( lines[len(lines) - 1] ) * (widest + 4)
        for i in range(len(lines)):
            line = lines[i]
            hpw = int(perpiece / 47) - 1 # 47 is 2f

            if i > 0:
                for j in range(len(line)):

                    # split node
                    c = ' '
                    if j % 2 == 1:
                        if line[j - 1] != None:
                            c = '┴' if (line[j] != None) else '┘'
                        else:
                            if j < len(line) and line[j] != None:
                                c = '└'
                    soprint += (c)

                    # lines and spaces
                    if line[j] == None:
                        soprint += (" " * int(perpiece-1))
                    else:

                        for k in range(hpw):
                            soprint += (" " if j % 2 == 0 else "─")
                            
                        soprint += ("┌" if j % 2 == 0 else "┐")
                        for k in range(hpw):
                            soprint += ("─" if j % 2 == 0 else " ")
                soprint += "\n"

            # print line of numbers
            for j in range(len(line)):

                f = line[j]
                if f == None:
                    f = ""
                med = perpiece / 47 - len(f) / 47
                gap1 = int(med)+1 if int(med) < med else int(med)
                gap2 = int(med) if int(med) < med else int(med)+1

                # a number
                soprint += (" " * gap1)
                soprint += (f)
                soprint += (" " * gap2)
            soprint += "\n"
            perpiece /= 2
            perpiece = int(perpiece)
        print(soprint)
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
    def __init__(self, index, isrbt):
        self.index = index
        self.isrbt = isrbt
        self.root = None
    def rotate(self, root, right = True):
        if root is None:
            return
        pivot = root.l if right else root.r
        if pivot is None:
            return
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
        if root.p is not None:
            if root is root.p.l:
                root.p.l = pivot
            else:
                root.p.r = pivot
        else:
            self.root = pivot
        root.p = pivot
    def gc(self, n): # get color
        return black if n is None else n.color
    def recolor(self, n):
        if n is None or self.gc(n.p) == black:
            return
        left = n is n.p.l
        uncle = None
        if n.p.p is not None:
            uncle = n.p.p.r if left else n.p.p.l
            n.p.p.color = red
        n.p.color = black
        if self.gc(uncle) == red:
            uncle.color = black
            if n.p.p is not None:
                self.recolor(n.p.p)
                print("recoloring")
        elif n.p.p is not None:
            self.rotate(n.p.p, left) # rotate left if n is left child. right if not
            print("rotating")
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
                    else:
                        now.r = n
                    break
            if self.isrbt:
                self.recolor(n)
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
    import sys
    # set this
    is_red_black_tree = True
    sort_by = sys.argv[1] # "id"


    ss = []
    ssfile = open("ss.txt", "r")
    ssl = ssfile.readlines()
    ssfile.close()
    for l in ssl:
        l = l.split('\n')[0].split(",")
        ss.append({ "id": l[0], "name": l[1], "lastname": l[2] })
    tree = rbt(sort_by, is_red_black_tree)
    for s in ss:
        tree.add(s)
    tree.root.printrb()
    print("-"*100)
    tree.root.print(sort_by)
    # tree.rotate(tree.root.r.r, False)
    # tree.rotate(tree.root.r.r, False)
    # print("-"*100)
    # tree.root.print(sort_by)
    # while True:
    #     print(">{}".format(tree.find(input(">>>"))))