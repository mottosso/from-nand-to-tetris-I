### Week 1

Reflecting on past week, where it was explained how `AND`, `NOT` and `OR` was all you would ever need to build any computer capable of computing anything and how each of these could be further reduced to a single gate called `NAND`; for *not* `AND`.

```bash
     ____
--->|     \
    |      |o----->
--->|_____/

```

From `NAND`, a `NOT` gate could be constructed by simply feeding it the input twice.

```qml
NOT(x) = NAND(x, x)
```

And from there, an `AND` gate was constructed by simply negating the output from `NAND`!

```qml
AND(x, y) = NOT(NAND(x, y))
```

How about `OR`?

```qml
OR(x, y) = NAND(NOT(x), NOT(y))
```

Genius!

All other possible gates; `XOR`, `MUX`, `DMUX` and so on can then be constructed by building upon the gates built before them. An entirety of a computer ultimately built upon 1 simple logic gate; the `NAND`.

#### Creating complex gates

The full definition of a gate can be given in at least 3 forms.

1. Formula
2. Truth table
3. Diagram

With any or all of these, a gate can be written in a HDL. Let's look at how to build an `XOR` gate.

First, here is the `XOR` truth table.

```bash
| x | y | out |
|---|---|-----|
| 0 | 0 |  1  |
| 0 | 1 |  0  |
| 1 | 0 |  0  |
| 1 | 1 |  1  |
```

From this truth table, we will construct formulas everywhere `out` = 1.

```bash
| x | y | out |
|---|---|-----|
| 0 | 0 |  1  | --> (NOT(x) AND NOT(y))
| 0 | 1 |  0  |
| 1 | 0 |  0  |
| 1 | 1 |  1  | --> (x AND y)
```

Both of these formulas yield 1 only and only at this particular row; that is, only when `x` and `y` equals these particular values.

All that's left now is `OR`ing them together!

```bash
XOR = (NOT(x) AND NOT(y)) OR (x AND y)
```

We can use boolean logic to simplfy a formula.

1. Commutative Laws
    Independent ordering.

  ```
(x AND y) = (y AND x)
(x OR y) = (y OR x)
```

2. Associative Laws
    `AND` relationships.

  ```
(x AND (y AND  z)) = ((x AND y) and z)
(x OR (y OR z)) = ((x OR y) OR z)
```

3. Distributive Laws
    `OR` relationships.

  ```
(x AND (y OR z)) = (x AND y) OR (x AND z)
(x OR (y AND z)) = (x OR y) AND (x OR z)
```

4. De Morgan Laws
   `NOT` relationship with `AND` and `OR`.

  ```
NOT(x AND y) = NOT(x) OR NOT(y)
NOT(x OR y) = NOT(x) AND NOT(y)
```

For example, consider this.

```
NOT(NOT(x) AND NOT(x OR y)) =           <--- De Morgan law
NOT(NOT(x) AND (NOT(x) AND NOT(y))) =   <--- Associative law
NOT((NOT(x) AND NOT(x)) AND NOT(y)) =   <--- NOT(x) AND NOT(x) = NOT(x)
NOT(NOT(x) AND NOT(y)) =                <--- De Morgan law
NOT(x) OR NOT(y) =                      <--- 0 OR 1 = 1 OR 0, Common sense.
x OR y                                  <--- Result
```