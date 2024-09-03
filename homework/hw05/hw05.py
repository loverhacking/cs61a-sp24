def hailstone(n):
    """Q1: Yields the elements of the hailstone sequence starting at n.
       At the end of the sequence, yield 1 infinitely.

    >>> hail_gen = hailstone(10)
    >>> [next(hail_gen) for _ in range(10)]
    [10, 5, 16, 8, 4, 2, 1, 1, 1, 1]
    >>> next(hail_gen)
    1
    """
    "*** YOUR CODE HERE ***"
  
    yield n
    if n == 1:
        yield from hailstone(1)
    elif n % 2 == 0:
        yield from hailstone(n // 2)
    else:
        yield from hailstone(n * 3 + 1)
  



def merge(a, b):
    """Q2:
    >>> def sequence(start, step):
    ...     while True:
    ...         yield start
    ...         start += step
    >>> a = sequence(2, 3) # 2, 5, 8, 11, 14, ...
    >>> b = sequence(3, 2) # 3, 5, 7, 9, 11, 13, 15, ...
    >>> result = merge(a, b) # 2, 3, 5, 7, 8, 9, 11, 13, 14, 15
    >>> [next(result) for _ in range(10)]
    [2, 3, 5, 7, 8, 9, 11, 13, 14, 15]
    """
    "*** YOUR CODE HERE ***"
    a_next = next(a)
    b_next = next(b)
    while True:
      if a_next == b_next:
            yield a_next
            a_next = next(a)
            b_next = next(b)
      elif a_next < b_next:
            yield a_next
            a_next = next(a)
      elif a_next > b_next:
            yield b_next
            b_next = next(b)

def sequence(start, step):
    while True:
         yield start
         start += step
a = sequence(2, 3) # 2, 5, 8, 11, 14, ...
b = sequence(3, 2) # 3, 5, 7, 9, 11, 13, 15, ...
result = merge(a, b) # 2, 3, 5, 7, 8, 9, 11, 13, 14, 15
[next(result) for _ in range(10)]


def yield_paths(t, value):
    """Q4: Yields all possible paths from the root of t to a node with the label
    value as a list.

    >>> t1 = tree(1, [tree(2, [tree(3), tree(4, [tree(6)]), tree(5)]), tree(5)])
    >>> print_tree(t1)
    1
      2
        3
        4
          6
        5
      5
    >>> next(yield_paths(t1, 6))
    [1, 2, 4, 6]
    >>> path_to_5 = yield_paths(t1, 5)
    >>> sorted(list(path_to_5))
    [[1, 2, 5], [1, 5]]

    >>> t2 = tree(0, [tree(2, [t1])])
    >>> print_tree(t2)
    0
      2
        1
          2
            3
            4
              6
            5
          5
    >>> path_to_2 = yield_paths(t2, 2)
    >>> sorted(list(path_to_2))
    [[0, 2], [0, 2, 1, 2]]
    """
    if label(t) == value:
        yield [value]
    for b in branches(t):
        for x in yield_paths(b, value):
              yield [label(t)] + x




# Tree Data Abstraction

def tree(label, branches=[]):
    """Construct a tree with the given label value and a list of branches."""
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

def label(tree):
    """Return the label value of a tree."""
    return tree[0]

def branches(tree):
    """Return the list of branches of the given tree."""
    return tree[1:]

def is_tree(tree):
    """Returns True if the given tree is a tree, and False otherwise."""
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    """Returns True if the given tree's list of branches is empty, and False
    otherwise.
    """
    return not branches(tree)

def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

def copy_tree(t):
    """Returns a copy of t. Only for testing purposes.

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(label(t), [copy_tree(b) for b in branches(t)])


###############
# Exam Practice
###############


# from Summer 2018 Final Q7a,b: Streams and Jennyrators
def generate_constant(x):
    """A generator function that repeats the same value X forever.
    >>> two = generate_constant(2)
    >>> next(two)
    2
    >>> next(two)
    2
    >>> sum([next(two) for _ in range(100)])
    200
    """
    yield x
    yield from generate_constant(x)

def black_hole(seq, trap):
    """A generator that yields items in SEQ until one of them matches TRAP, in
    which case that value should be repeatedly yielded forever.
    >>> trapped = black_hole([1, 2, 3], 2)
    >>> [next(trapped) for _ in range(6)]
    [1, 2, 2, 2, 2, 2]
    >>> list(black_hole(range(5), 7))
    [0, 1, 2, 3, 4]
    """
    for item in seq:
      if item == trap:
        yield from generate_constant(trap)
      else:
        yield item

# from Spring 2021 MT2 Q8: The Tree of L-I-F-E
def word_finder(letter_tree, words_list):
    """ Generates each word that can be formed by following a path
    in TREE_OF_LETTERS from the root to a leaf,
    where WORDS_LIST is a list of allowed words (with no duplicates).
    # Case 1: 2 words found
    >>> words = ['SO', 'SAT', 'SAME', 'SAW', 'SOW']
    >>> t = tree("S", [tree("O"), tree("A", [tree("Q"), tree("W")]), tree("C", [tree("H")])])
    >>> gen = word_finder(t, words)
    >>> next(gen)
    'SO'
    >>> next(gen)
    'SAW'
    >>> list(word_finder(t, words))
    ['SO', 'SAW']

    # Case 2: No words found
    >>> t = tree("S", [tree("I"), tree("A", [tree("Q"), tree("E")]), tree("C", [tree("H")])])
    >>> list(word_finder(t, words))
    []

    # Case 3: Same word twice
    >>> t = tree("S", [tree("O"), tree("O")] )
    >>> list(word_finder(t, words))
    ['SO', 'SO']

    # Case 4: Words that start the same
    >>> words = ['TAB', 'TAR', 'BAT', 'BAR', 'RAT']
    >>> t = tree("T", [tree("A", [tree("R"), tree("B")])])
    >>> list(word_finder(t, words))
    ['TAR', 'TAB']

    # Case 5: Single letter words
    >>> words = ['A', 'AN', 'AH']
    >>> t = tree("A")
    >>> list(word_finder(t, words))
    ['A']

    # Case 6: Words end in leaf
    >>> words = ['A', 'AN', 'AH']
    >>> t = tree("A", [tree("H"), tree("N")])
    >>> list(word_finder(t, words))
    ['AH', 'AN']

    # Case 7: Words start at root
    >>> words = ['GO', 'BEARS', 'GOB', 'EARS']
    >>> t = tree("B", [tree("E", [tree("A", [tree("R", [tree("S")])])])])
    >>> list(word_finder(t, words))
    ['BEARS']

    # Case 8: This special test ensures that your solution does *not*
    # pre-compute all the words before yielding the first one.
    # If done correctly, your solution should error only when it
    # tries to find the second word in this tree.
    >>> words = ['SO', 'SAM', 'SAT', 'SAME', 'SAW', 'SOW']
    >>> t = tree("S", [tree("O"), tree("A", [tree("Q"), tree(1)]), tree("C", [tree(1)])])
    >>> gen = word_finder(t, words)
    >>> next(gen)
    'SO'
    >>> try:
    ...   next(gen)
    ... except TypeError:
    ...   print("Got a TypeError!")
    ... else:
    ...   print("Expected a TypeError!")
    Got a TypeError!
    """
    def helper(t, word):
      word = word + label(t) # Optional
      if word in words_list and is_leaf(t):
        yield word
      for b in branches(t):
        yield from helper(b, word) 
    yield from helper(letter_tree, '')


# from Summer 2016 Final Q8: Zhen-erators Produce Power
def integers(n):
    while True:
      yield n
      n += 1

def drop(n, s):
    for _ in range(n):
      next(s)
    for elem in s:
      yield elem

def powers_of_two(ints=integers(0)):
  """
  >>> p = powers_of_two()
  >>> [next(p) for _ in range(10)]
  [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
  """
  curr = pow(2, next(ints))
  yield curr
  yield from powers_of_two()

# from Spring 2018 Final Q4a: Apply Yourself
def times(f, x):
    """Return a function g(y) that returns the number of f's in f(f(...(f(x)))) == y.
    >>> times(lambda a: a + 2, 0)(10) # 5 times: 0 + 2 + 2 + 2 + 2 + 2 == 10
    5
    >>> times(lambda a: a * a, 2)(256) # 3 times: square(square(square(2))) == 256
    3
    """
    def repeat(z):
      """Yield an infinite sequence of z, f(z), f(f(z)), f(f(f(z))), f(f(f(f(z)))), ...."""
      yield z
      yield from repeat(f(z))
    def g(y):
      n = 0
      for w in repeat(x):
        if w == y:
          return n
        n = n + 1
    return g