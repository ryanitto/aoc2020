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

========================================

--- Part Two ---

It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number
of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

faded blue bags contain 0 other bags.
dotted black bags contain 0 other bags.
vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.

So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and
the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count
all of the bags, even if the nesting becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.

In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?

========================================

Your puzzle answer was 11261.

Both parts of this puzzle are complete! They provide two gold stars: **

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
        return f'{self.name}: (Children: {self.children}, Parents: {self.parents})'


class Solve:
    _bags = []
    _bags_to_names = {}

    my_bag = 'shiny gold'
    count = 0

    def __init__(self, **kwargs):
        for k, v in kwargs:
            setattr(self, k, v) if hasattr(self, k) else None

    @staticmethod
    def get_total_bags_from_bag(bag):
        totals = []

        def get_totals(bag, subtotals):
            mult = 1
            if any(subtotals):
                mult = subtotals[-1]
            for b, count in bag.children.items():
                subtotals.append(int(count) * mult)
                get_totals(b, subtotals)
            return subtotals

        totals = get_totals(bag, totals)
        return sum(totals)

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

        return self._bags

    def go(self, part_one=False):
        """
        Do the solve!  If you want part one, change the keyword to true. :)

        :param part_one: (bool) If True, do the first part of the puzzle
        :return: (int) result of either puzzle
        """

        self.parse_rules(lines, rule_text=CONTAIN_KEY)
        my_bag = self._bags_to_names[self.my_bag]

        if part_one:
            return len(self.get_parents_for_bag(my_bag))
        else:
            return self.get_total_bags_from_bag(my_bag)


if __name__ == '__main__':
    print(Solve().go())
