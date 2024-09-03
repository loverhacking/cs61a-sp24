passphrase = '*** PASSPHRASE HERE ***'


def midsem_survey(p):
    """
    You do not need to understand this code.
    >>> midsem_survey(passphrase)
    '3d9f1125b109b311959d068240016badb874603eab75302a445e1a50'
    """
    import hashlib
    return hashlib.sha224(p.encode('utf-8')).hexdigest()


class VendingMachine:
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Nothing left to vend. Please restock.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'Please add $10 more funds.'
    >>> v.add_funds(7)
    'Current balance: $7'
    >>> v.vend()
    'Please add $3 more funds.'
    >>> v.add_funds(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.add_funds(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.restock(3)
    'Current soda stock: 6'
    >>> w.add_funds(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """
    "*** YOUR CODE HERE ***"

    def __init__(self, product, price):
        self.product = product
        self.price = price
        self.balance = 0
        self.num = 0

    def vend(self):
        if self.num == 0:
            return 'Nothing left to vend. Please restock.'
        elif self.num > 0 and self.balance < self.price:
            return f'Please add ${str(self.price - self.balance)} more funds.'
        elif self.num > 0 and self.balance == self.price:
            self.num = self.num - 1
            self.balance = 0
            return f'Here is your {str(self.product)}.'
        elif self.num > 0 and self.balance > self.price:
            self.num = self.num - 1
            change = self.balance - self.price
            self.balance = 0
            return f'Here is your {self.product} and ${str(change)} change.'

    def add_funds(self, n):
        if self.num:
            self.balance = self.balance + n
            return f'Current balance: ${self.balance}'
        return f'Nothing left to vend. Please restock. Here is your ${str(n)}.'

    def restock(self, n):
        self.num = self.num + n
        return f'Current {self.product} stock: {str(self.num)}'


def store_digits(n):
    """Stores the digits of a positive number n in a linked list.

    >>> s = store_digits(1)
    >>> s
    Link(1)
    >>> store_digits(2345)
    Link(2, Link(3, Link(4, Link(5))))
    >>> store_digits(876)
    Link(8, Link(7, Link(6)))
    >>> store_digits(2450)
    Link(2, Link(4, Link(5, Link(0))))
    >>> # a check for restricted functions
    >>> import inspect, re
    >>> cleaned = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(store_digits)))
    >>> print("Do not use str or reversed!") if any([r in cleaned for r in ["str", "reversed"]]) else None
    """
    "*** YOUR CODE HERE ***"
    s = Link.empty
    while n > 0:
        s = Link(n % 10, s)
        n //= 10
    return s


def deep_map_mut(func, lnk):
    """Mutates a deep link lnk by replacing each item found with the
    result of calling func on the item. Does NOT create new Links (so
    no use of Link's constructor).

    Does not return the modified Link object.

    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    >>> print(link1)
    <3 <4> 5 6>
    >>> # Disallow the use of making new Links before calling deep_map_mut
    >>> Link.__init__, hold = lambda *args: print("Do not create any new Links."), Link.__init__
    >>> try:
    ...     deep_map_mut(lambda x: x * x, link1)
    ... finally:
    ...     Link.__init__ = hold
    >>> print(link1)
    <9 <16> 25 36>
    """
    "*** YOUR CODE HERE ***"
    if lnk is Link.empty:
        return
    elif isinstance(lnk.first, int):
        lnk.first = func(lnk.first)
    else:
        deep_map_mut(func, lnk.first)
    deep_map_mut(func, lnk.rest)


def two_list(vals, counts):
    """
    Returns a linked list according to the two lists that were passed in. Assume
    vals and counts are the same size. Elements in vals represent the value, and the
    corresponding element in counts represents the number of this value desired in the
    final linked list. Assume all elements in counts are greater than 0. Assume both
    lists have at least one element.
    >>> a = [1, 3]
    >>> b = [1, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(3))
    >>> a = [1, 3, 2]
    >>> b = [2, 2, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(1, Link(3, Link(3, Link(2)))))
    """
    "*** YOUR CODE HERE ***"
    if not vals:
        return Link.empty
    counts[0] -= 1
    if counts[0] == 0:
        return Link(vals[0], two_list(vals[1:], counts[1:]))
    return Link(vals[0], two_list(vals, counts))


class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'


###############
# Exam Practice
###############

#############################
# Object-Oriented Programming
#############################

# from Spring 2022 MT2 Q8: CS61A Presents The Game of Hoop.
class HoopPlayer:
    def __init__(self, strategy):
        """Initialize a player with STRATEGY, and a starting SCORE of 0. The
        STRATEGY should be a function that takes this player's score and a list
        of other players' scores.
        """
        self.strategy = strategy
        self.score = 0


class HoopDice:
    def __init__(self, values):
        """Initialize a dice with possible values VALUES, and a starting INDEX
        of 0. The INDEX indicates which value from VALUES to return when the
        dice is rolled next.
        """
        self.values = values
        self.index = 0

    def roll(self):
        """Roll this dice. Advance the index to the next step before
        returning.
        >>> five_six = HoopDice([5, 6])
        >>> five_six.roll()
        5
        >>> five_six.index
        1
        >>> five_six.roll()
        6
        >>> five_six.index
        0
        """

        value = self.values[self.index]
        # (1a)
        self.index = (self.index + 1) % len(self.values)
        # (1b)       (1c)                (1d)
        return value


class HoopGame:
    """
    In all following subparts, assume that the following has already been run to set up the game:
    >>> roll_once_strategy = lambda pl, ops: 1
    >>> roll_twice_strategy = lambda pl, ops: 2
    >>> always_5 = HoopDice([5])
    >>> player1 = HoopPlayer(roll_twice_strategy)
    >>> player2 = HoopPlayer(roll_once_strategy)
    >>> player3 = HoopPlayer(lambda pl, ops: 6)
    >>> game = HoopGame([player1, player2, player3], always_5, 55)
    >>>  # since we omit the implementation of HoopGame.get_scores, here's what it
    >>>  # should output:
    >>> game.get_scores()
    [0, 0, 0]
    """

    def __init__(self, players, dice, goal):
        """Initialize a game with a list of PLAYERS, which contains at least one
        HoopPlayer, a single HoopDice DICE, and a goal score of GOAL.
        """
        self.players = players
        self.dice = dice
        self.goal = goal

    def next_player(self):
        """Infinitely yields the next player in the game, in order.
        >>> next(player_gen) is player1
        True
        >>> next(player_gen) is player3
        False
        >>> next(player_gen) is player3
        True
        >>> next(player_gen) is player1
        True
        >>> next(player_gen) is player2
        True
        >>> new_player_gen = game.next_player()
        >>> next(new_player_gen) is player1
        True
        >>> next(player_gen) is player3
        True
        """
        yield from self.players
        # (2a)
        yield from self.next_player()
        # (2b)

    def get_scores(self):
        """Collects and returns a list of the current scores for all players
        in the same order as the SELF.PLAYERS list.
        """

    # Implementation omitted. Assume this method works correctly

    def get_scores_except(self, player):
        """Collects and returns a list of the current scores for all players
        except PLAYER.
        >>> game.get_scores_except(player2)
        [0, 0]
        """

        return [pl.score for pl in self.players if pl is not player]
        # (3a)                (3b)             (3c)

    def roll_dice(self, num_rolls):
        """Simulate rolling SELF.DICE exactly NUM_ROLLS > 0 times. Return sum of
        the outcomes unless any of the outcomes is 1. In that case, return 1.
        >>> game.roll_dice(4)
        20
        """

        outcomes = [self.dice.roll() for x in range(num_rolls)]
        # (4a)                      (4b)
        ones = [outcome == 1 for outcome in outcomes]
        # (4c)
        return 1 if any(ones) else sum(outcomes)
        # (4d)            (4e)

    def play(self):
        """Play the game while no player has reached or exceeded the goal score.
        After the game ends, return all players' scores.
        >>> game.play()
        [20, 10, 60]
        """

        player_gen = self.next_player()
        while max(self.get_scores()) < self.goal:
            player = next(player_gen)
            # (5a)
            other_scores = self.get_scores_except(player)
            num_rolls = player.strategy(player.score, other_scores)
            # (5b)
            outcome = self.roll_dice(num_rolls)
            player.score += outcome
            # (5c)
        return self.get_scores()


class BrokenHoopDice(HoopDice):
    def __init__(self, values, when_broken):
        super().__init__(values)
        # (6a)
        self.when_broken = when_broken
        self.is_broken = False
        # (6b)

    def roll(self):
        """
        >>> broken = BrokenHoopDice([5, 6, 7], 11)
        >>> broken.roll()
        5
        >>> [broken.roll() for _ in range(6)]
        [11, 6, 11, 7, 11, 5]
        """
        if self.is_broken:
            self.is_broken = not self.is_broken
            return self.when_broken
            # (6c)
        else:
            self.is_broken = not self.is_broken
            return super().roll()
            # (6d)


# from Fall 2020 MT2 Q3: Sparse Lists
from collections import Counter


def most_common(s):
    """Return the most common element in non-empty list s. In case of a tie,
    return the most common element that appears first in s.
    >>> most_common([3, 1, 4, 1, 5, 9])
    1
    >>> most_common([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
    5
    >>> most_common([2, 7, 1, 8, 2, 8, 1, 8, 2, 8])
    8
    >>> most_common([3, 5, 7, 7, 7, 5, 5])
    5
    >>> most_common([3, 7, 5, 5, 7, 7])
    7
    """

    """Assume this function is implemented for you."""
    counts = Counter(s)
    most_frequent = counts.most_common(1)[0][0]
    return most_frequent


class SparseList:
    """Represent a non-empty list as a most common value and a dictionary from
    indices to values that contains only values that are not the most common.
    >>> pi = SparseList([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
    >>> pi.common
    5
    >>> pi.others
    {0: 3, 1: 1, 2: 4, 3: 1, 5: 9, 6: 2, 7: 6, 9: 3}
    >>> [pi.item(0), pi.item(1), pi.item(2), pi.item(3), pi.item(4)]
    [3, 1, 4, 1, 5]
    >>> pi.item(10)
    5
    >>> pi.item(11)
    'out of range'
    >>> pi.items()
    [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    """

    def __init__(self, s):
        assert s, 's cannot be empty'
        self.n = len(s)
        self.common = most_common(s)
        # (a)
        self.others = {i: s[i] for i in range(self.n) if s[i] != self.common}
        # (b)  (c)                  (d)            (e)

    def item(self, i):
        """Return s[i] or 'out of range' if i is not smaller than the length of s."""
        assert i >= 0, 'index i must be non-negative'
        if i >= self.n:
            # (a)
            return 'out of range'
        elif i in self.others:
            # (b)
            return self.others[i]
            # (c)
        else:
            return self.common

    def items(self):
        """Return a list with the same elements as s in the same order as s."""
        return [self.item(i) for i in range(self.n)]
        # (a)                (b)


# from Fall 2019 MT2 Q7: Version 2.0
class Version:
    """A version of a string after an edit.
    >>> s = Version('No power?', Delete(3, 6))
    >>> print(Version(s, Insert(3, 'class!')))
    No class!
    >>> t = Version('Beary', Insert(4, 'kele'))
    >>> print(t)
    Bearkeley
    >>> print(Version(t, Delete(2, 1)))
    Berkeley
    >>> print(Version(t, Delete(4, 5)))
    Bear
    """

    def __init__(self, previous, edit):
        self.previous, self.edit = previous, edit

    def __str__(self):
        return self.edit.apply(str(self.previous))


class Edit:
    def __init__(self, i, c):
        self.i, self.c = i, c


class Insert(Edit):
    def apply(self, t):
        "Return a new string by inserting string c into t starting at position i."
        return t[:self.i] + self.c + t[self.i:]


class Delete(Edit):
    def apply(self, t):
        "Return a new string by deleting c characters from t starting at position i."
        return t[:self.i] + t[self.i + self.c:]


##############
# Linked Lists
##############

# from Fall 2020 Final Q3: College Party


class State:
    electors = {}

    def __init__(self, code, electors):
        self.code = code
        self.electors = electors
        State.electors[code] = electors


battleground = [State('AZ', 11), State('PA', 20), State('NV', 6),
                State('GA', 16), State('WI', 10), State('MI', 16)]


def print_all(s):
    for x in s:
        print(x)


# (a)
def wins(states, k):
    """Yield each linked list of two-letter state codes that describes a win by at least k.
    >>> print_all(wins(battleground, 50))
    <AZ PA NV GA WI MI>
    <AZ PA NV GA MI>
    <AZ PA GA WI MI>
    <PA NV GA WI MI>
    >>> print_all(wins(battleground, 75))
    <AZ PA NV GA WI MI>
    """
    if k <= 0 and not states:
        # (a)
        yield Link.empty
    if states:
        first = states[0].electors
        for win in wins(states[1:], k - first):
            # (b)
            yield Link(states[0].code, win)
            # (c)
        yield from wins(states[1:], k + first)
        # (d)


# (b)
def must_win(states, k):
    """List all states that must be won in every scenario that wins by k.
    >>> must_win(battleground, 50)
    ['PA', 'GA', 'MI']
    >>> must_win(battleground, 75)
    ['AZ', 'PA', 'NV', 'GA', 'WI', 'MI']
    """

    def contains(s, x):
        """Return whether x is a value in linked list s."""
        return (s is not Link.empty) and (x == s.first or contains(s.rest, x))
        #           (a)                               (b)

    return [s.code for s in states if all([contains(w, s.code) for w in wins(states, k)])]
    #        (c)                      (d)              (e)


# (c)
def is_minimal(state_codes, k):
    """Return whether a non-empty list of state_codes describes a minimal win by
    at least k.
    >>> is_minimal(['AZ', 'NV', 'GA', 'WI'], 0) # Every state is necessary
    True
    >>> is_minimal(['AZ', 'GA', 'WI'], 0) # Not a win
    False
    >>> is_minimal(['AZ', 'NV', 'PA', 'WI'], 0) # NV is not necessary
    False
    >>> is_minimal(['AZ', 'PA', 'WI'], 0) # Every state is necessary
    True
    """
    assert state_codes, 'state_codes must not be empty'
    votes_in_favor = [State.electors[item] for item in state_codes]
    # (a)
    total_possible_votes = sum(State.electors.values())

    # (b)
    def win_margin(n):
        """Margin of victory if n votes are in favor and the rest are against."""
        return n - (total_possible_votes - n)

    if win_margin(sum(votes_in_favor)) < k:
        return False  # Not a win
    in_favor_no_smallest = sum(votes_in_favor) - min(votes_in_favor)
    # (c)
    return win_margin(in_favor_no_smallest) < k


# from Fall 2018 MT2 Q6: Dr. Frankenlink

def replace(s, t, i, j):
    """Replace the slice of s from i to j with t.
    >>> s, t = Link(3, Link(4, Link(5, Link(6, Link(7))))), Link(0, Link(1, Link(2)))
    >>> replace(s, t, 2, 4)
    >>> print(s)
    <3 4 0 1 2 7>
    >>> t.rest.first = 8
    >>> print(s)
    <3 4 0 8 2 7>
    """
    assert s is not Link.empty and t is not Link.empty and i > 0 and i < j
    if i > 1:
        replace(s.rest, t, i - 1, j - 1)
    else:  # i = 0
        for k in range(j - i):
            s.rest = s.rest.rest  # end of replace of s
        end = t
        while end.rest is not Link.empty:
            end = end.rest
        s.rest, end.rest = t, s.rest


# from Spring 2017 MT1 Q5: Insert
def link_insert(lnklst, value, before):
    """Return a linked list identical to LNKLST, but with VALUE inserted just
    before the first occurrence of BEFORE in the list, if any. The returned
    list is identical to LNKLST if BEFORE does not occur in LNKLST.
    The operation is non-destructive.
    >>> L = Link(2, Link(3, Link(7, Link(1))))
    >>> print(L)
    <2 3 7 1>
    >>> Q = link_insert(L, 19, 7)
    >>> print(Q)
    <2 3 19 7 1>
    >>> print(link_insert(L, 19, 20))
    <2 3 7 1>
    """
    if lnklst is Link.empty:
        return lnklst
    elif lnklst.first == before:
        return Link(value, lnklst)
    else:
        return Link(lnklst.first, link_insert(lnklst.rest, value, before))
