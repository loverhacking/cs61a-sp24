CREATE TABLE parents AS
  SELECT "abraham" AS parent, "barack" AS child UNION
  SELECT "abraham"          , "clinton"         UNION
  SELECT "delano"           , "herbert"         UNION
  SELECT "fillmore"         , "abraham"         UNION
  SELECT "fillmore"         , "delano"          UNION
  SELECT "fillmore"         , "grover"          UNION
  SELECT "eisenhower"       , "fillmore";

CREATE TABLE dogs AS
  SELECT "abraham" AS name, "long" AS fur, 26 AS height UNION
  SELECT "barack"         , "short"      , 52           UNION
  SELECT "clinton"        , "long"       , 47           UNION
  SELECT "delano"         , "long"       , 46           UNION
  SELECT "eisenhower"     , "short"      , 35           UNION
  SELECT "fillmore"       , "curly"      , 32           UNION
  SELECT "grover"         , "short"      , 28           UNION
  SELECT "herbert"        , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT child from parents, dogs
    where parent = name order by height DESC;


-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT name, size from dogs, sizes 
    where height > min and height <= max;


-- Filling out this helper table is optional
CREATE TABLE siblings AS
  SELECT a.child as first, b.child as second 
    from parents as a, parents as b
    where a.parent = b.parent and a.child < b.child; 
  
-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT 'The two siblings, ' || first || ' and '|| second || ', have the same size: ' || a.size 
    from siblings, size_of_dogs as a, size_of_dogs as b
    where a.size = b.size and a.name = first and b.name = second;


-- Height range for each fur type where all of the heights differ by no more than 30% from the average height
CREATE TABLE low_variance AS
  SELECT fur, max(height) - min(height) 
    from dogs group by fur
    having min(height) >= 0.7 * avg(height) and max(height) <= 1.3 * avg(height);

-- from Fall 2019 Final, Question 10: Big Game
CREATE TABLE scoring AS
  SELECT "Donald Stewart" AS player, 7 AS points, 1 AS quarter UNION
  SELECT "Christopher Brown Jr.",    7,           1            UNION
  SELECT "Ryan Sanborn",             3,           2            UNION
  SELECT "Greg Thomas",              3,           2            UNION
  SELECT "Cameron Scarlett",         7,           3            UNION
  SELECT "Nikko Remigio",            7,           4            UNION
  SELECT "Ryan Sanborn",             3,           4            UNION
  SELECT "Chase Garbers",            7,           4;

CREATE TABLE players AS
  SELECT "Ryan Sanborn" AS name,  "Stanford" AS team UNION
  SELECT "Donald Stewart",        "Stanford"         UNION
  SELECT "Cameron Scarlett",      "Stanford"         UNION
  SELECT "Christopher Brown Jr.", "Cal"              UNION
  SELECT "Greg Thomas",           "Cal"              UNION
  SELECT "Nikko Remigio",         "Cal"              UNION
  SELECT "Chase Garbers",         "Cal";

--- (a)
SELECT quarter FROM scoring
  GROUP BY quarter HAVING SUM(points) > 10

--- (b)
SELECT team, SUM(points) FROM scoring, players
  WHERE name = player GROUP BY team;

--- from Summer 2019 Final, Question 8: The Big SQL
CREATE TABLE ingredients AS
  SELECT "chili" AS dish, "beans" AS part UNION
  SELECT "chili" ,        "onions"        UNION
  SELECT "soup" ,         "broth"         UNION
  SELECT "soup" ,         "onions"        UNION
  SELECT "beans" ,        "beans";

CREATE TABLE shops AS
  SELECT "beans" AS food, "A" AS shop, 2 AS price UNION
  SELECT "beans" ,        "B" ,        2 AS price UNION
  SELECT "onions" ,       "A" ,        3          UNION
  SELECT "onions" ,       "B" ,        2          UNION
  SELECT "broth" ,        "A" ,        3          UNION
  SELECT "broth" ,        "B" ,        5;

--- (a)
SELECT food, MIN(price) FROM shops GROUP BY food;

--- (b)
SELECT dish,  SUM(price) FROM ingredients, shops
  WHERE shop = 'A' AND part = food GROUP BY dish;

--- (c)
SELECT a.food FROM shops AS a, shops AS b
  WHERE a.food = b.food AND a.price > b.price;

SELECT food FROM shops GROUP BY food HAVING MIN(price) < MAX(price);


---from Fall 2018 Final, Question 7: SQL of Course

CREATE TABLE courses AS
  SELECT "1" AS course, 14 AS h, 0 AS m, 80 AS len UNION
  SELECT "2" ,          13 ,     30 ,    80        UNION
  SELECT "8" ,          12 ,     30 ,    50        UNION
  SELECT "10" ,         12 ,     30 ,    110       UNION
  SELECT "50AC" ,       13 ,     30 ,    45        UNION
  SELECT "61A" ,        13 ,     0 ,     50;

CREATE TABLE locations AS
  SELECT "1" AS name, "VLSB" AS loc UNION
  SELECT "2" ,        "Dwinelle"    UNION
  SELECT "10" ,       "VLSB"        UNION
  SELECT "50AC" ,     "Wheeler"     UNION
  SELECT "61A" ,      "Wheeler";

--- (a)
SELECT course FROM courses WHERE h <13 OR (h = 13 AND m < 30) ;

--- (b)
SELECT loc, min(len)
  FROM courses, locations WHERE course = name
  GROUP BY loc

--- (c)
SELECT first.course , second.course, 
  second.h * 60 + second.m -  (first.h * 60 + first.m  + first.len) AS gap
  FROM courses AS first, courses AS second
  where gap > 0;