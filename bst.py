


class rbt:
    def __init__(self, init_list, index = "id"):
        self.index = index
        self.tree = {}
        for i in init_list:
            self.insert(i)
    def __rewire(self, frm, to, save, obj = None):
        level = 0
        base_from = frm
        base_to = to
        flag = True
        while flag:
            flag = False
            for i in range(2**level):
                if obj is not None and obj.get(base_from + i) is not None:
                    flag = True
                    save[base_to + i] = (obj[base_from + i][0], obj[base_from + i][1], base_to + i)
                elif self.get(base_from + i) is not None:
                    flag = True
                    save[base_to + i] = (self.get(base_from + i)[0], self.color(base_from + i), base_to + i)
            base_from = base_from * 2 + 1
            base_to = base_to * 2 + 1
            level += 1
    def __pick(self, root, base):
        level = 0
        flag = True
        while flag:
            flag = False
            for i in range(2**level):
                if base.get(root + i) is not None:
                    flag = True
                    base.pop(root + i)
            root = root * 2 + 1
            level += 1
    def __rotate(self, root, right = True):
        #     root   rotate->right
        #   /      \
        # pivot   base
        #   \      /
        #   bee  honey
        new = {}
        pivot = self.l(root) if right else self.r(root)
        base = self.r(root) if right else self.l(root)
        bee = self.r(pivot) if right else self.l(pivot)
        honey = self.l(base) if right else self.r(base)
        # push down :
        self.__rewire(base, self.r(base) if right else self.l(base), new)
        new[base] = (self.get(root)[0], self.color(root), base)
        # bee to honey:
        self.__rewire(bee ,honey, new)
        # pull up :
        self.__pick(bee ,self.tree)
        self.__rewire(pivot, root, new)
        # append(new)
        self.__rewire(root, root, self.tree, new)
        
    def __recolor(self, v):
        # TO DEBUG
        RED = 1
        BLACK = 0
        p = self.p(v)
        if self.get(p) is None or self.color(p) == BLACK:
            return
        grand_p = self.p(p)
        is_left = p % 2 == 0
        uncle = p + 1 if is_left else p - 1
        self.color(p, BLACK)
        self.color(grand_p, RED)
        if self.color(uncle) == RED:
            self.color(uncle, BLACK)
            self.__recolor(grand_p)
        else: # uncle.color = black
            self.__rotate(grand_p, is_left) # grandpa rotate right if dad is left rotate left if dad is right
    def insert(self, item):
        RED = 1
        BLACK = 0
        now = 0
        while self.get(now) is not None:
            if self.key(now) != item[self.index]: # now.id != item.id
                now = self.find(item[self.index], now)
            else:
                now = self.find(item[self.index], self.r(now))

        if now == 0: # now is root
            self.tree[now] = (item, BLACK, now)
        else:
            self.tree[now] = (item, RED, now)
            self.__recolor(now)
    def delete(self, item):
        pass
    def find(self, target, root = 0):
        while self.get(root) is not None:
            now = self.key(root)
            if now == target:
                return root
            elif now < target:
                root = self.r(root)
                continue
            else:
                root = self.l(root)
                continue
        return root
    def color(self, idx, new = None):
        if new is not None and self.get(idx) is not None:
            self.tree[idx] = (self.get(idx)[0], new, idx)
        return self.get(idx)[1] if self.get(idx) is not None else 0 # 0:black
    def key(self, idx):
        return self.get(idx)[0][self.index] if self.get(idx) is not None else None
    def get(self, idx):
        return (self.tree[idx][0], self.tree[idx][1], idx) if self.tree.get(idx) is not None else None
    def l(self, node):
        return node*2+1
    def r(self, node):
        return node*2+2
    def p(self, node):
        return (int)((node-1)/2)
    def root(self):
        return 0

stu = [
    { "id":12 },
    { "id":2 },
    { "id":3 },
    { "id":0 },
    { "id":4 },
    { "id":8 },
    { "id":5 }
]
tree = rbt(stu, "id")
# for i in range(len(stu)):
#     print(i, tree.get(tree.find(i)))
for i in tree.tree:
    print(i, "RED" if tree.tree[i][1] == 1 else "BLACK", tree.tree[i][0]['id']) #, tree.tree[i][0]['name'], tree.tree[i][0]['last']
# print(tree.get(tree.p(tree.r(tree.r(tree.root())))))