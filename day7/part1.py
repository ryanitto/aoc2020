"""
--- Day 7: Handy Haversacks ---

You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab
some food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents;
bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently,
nobody responsible for these regulations considered how long they would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.

These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty,
every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would
be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

- A bright white bag, which can hold your shiny gold bag directly.
- A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
- A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold
bag.
- A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold
bag.

So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure
you get all of it.)

========================================

Your puzzle answer was 131.

The first half of this puzzle is complete! It provides one gold star: *
"""
import input_

file_ = input_.get_input_file(__file__)
lines = input_.get_lines(file_)

BAG_KEY = 'bag'
CONTAIN_KEY = f'{BAG_KEY}s contain'
NULL_KEY = f'no other {BAG_KEY}s'


class Bag:
    name = ''
    children = {}
    parents = []

    def __init__(self, name, children=None):
        self.name = name
        if children:
            self.children = children if any(children) else []

    def __repr__(self):
        return self.name

    def __str__(self):
        # return f'{self.name}: (Children: {self.children})'
        return f'{self.name}: (Parents: {self.parents})'


class Solve:
    _bags = []
    _bags_to_names = {}

    my_bag = 'shiny gold'

    def __init__(self, **kwargs):
        for k, v in kwargs:
            setattr(self, k, v) if hasattr(self, k) else None
    
    def get_children_from_desc(self, desc):
        children = {}

        if desc == NULL_KEY:
            pass
        else:
            split_children = desc.split(', ')
            for c in split_children:
                child_bag_desc = c.split(' ')[:-1]
                child_bag_count = child_bag_desc[0]
                child_bag_name = ' '.join(child_bag_desc[1:])
                child_bag = self._bags_to_names[child_bag_name]
                children[child_bag] = child_bag_count

        return children

    def get_parents_for_bag(self, bag):
        parents = []

        def get_parents(self, parent_bag):
            for b in self._bags:
                if parent_bag in b.children:
                    parents.append(b)
                    get_parents(self, b)

        get_parents(self, bag)
        return list(set(parents))

    def parse_rule(self, line, rule_text=''):
        name, children_desc = [l.strip().replace('.', '') for l in line.split(rule_text)]
        return name, children_desc

    def parse_rules(self, lines, rule_text=''):
        parsed = [self.parse_rule(l, rule_text=rule_text) for l in lines]
        self._bags = [Bag(n[0]) for n in parsed]
        self._bags_to_names = {b.name: b for b in self._bags}

        for p in parsed:
            bag, desc = p
            if bag in self._bags_to_names:
                # Get children from description, keep count of how many potential children, too
                children = self.get_children_from_desc(desc)

                # Add children, to this bag
                bag_object = self._bags_to_names[bag]
                bag_object.children = children

        # parent_names_of_children_dict = {k.name: [v.name for v in k.children] for k in self._bags}
        # children_of_parents_dict = {}
        #
        # for parent, children in parent_names_of_children_dict.items():
        #     for c in children:
        #         print(c)

        return self._bags

    def go(self):
        self.parse_rules(lines, rule_text=CONTAIN_KEY)
        my_bag = self._bags_to_names[self.my_bag]
        return len(self.get_parents_for_bag(my_bag))


if __name__ == '__main__':
    print(Solve().go())
