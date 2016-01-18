### Binary Addition

Once we have addition, subtraction is free thanks to two's complement.

Here's traditional addition, the one you know from school.

```
 1
  931
+ 153
-----
 1084
```

The addition involves a "carry" when the result of adding two numbers *overflows* the space available for storage. The overflow is passed on to the next computation, which in this case simply is 0.

Binary addition works in much the same way.

```
      1
  010001
+ 100001
--------
  110010
```

<br>
<br>
<br>

#### Half Adder

The *half adder* takes two numbers and adds them together, without taking into consideration any previous carry. This is great for calculating the first number, because the carry is always 0.

```bash
     0
  ????1?
+ ????0?
--------
      1
```

Here is the truth table for the Half Adder.

```
a b | sum carry
----|----------
0 0 |  0    0
0 1 |  1    0
1 0 |  1    0
1 1 |  0    1
```

When there are two outputs in a truth table, we can consider each in turn where the result of each the output.

```
a b | sum carry
----|----------
0 0 |  0    0
0 1 |  1    0 --> NOT(a) AND b
1 0 |  1    0 --> a AND NOT(b)
1 1 |  0    1 
```

That's the value of `sum`.

```
a b | sum carry
----|----------
0 0 |  0    0
0 1 |  1    0
1 0 |  1    0
1 1 |  0    1 --> a AND b 
```

And that's the value of `carry`.

If we take a closer look at the truth table for just `a`, `b` and `sum` we'll find a remarkable resemblance.

```
a b | sum
----|----
0 0 |  0 
0 1 |  1 
1 0 |  1 
1 1 |  0 
```

That's the same as `XOR` from above!

Which means we can replace that whole ugly formula, with `XOR`, resulting in.

```
XOR(a=a, b=b, out=sum)
AND(a=a, b=b, out=carry)
```

Now I mentioned that the Half Adder does *not* take into account the carry from previous addition, so it is in essence only half done.

<br>
<br>
<br>

#### Full Adder

The Full Adder takes into account a carry from a previous operation, closing the loop on any addition operation.

```
a b c | sum carry
------|----------
0 0 0 |  0    0
0 0 1 |  1    0
0 1 0 |  1    0
0 1 1 |  0    1
1 0 0 |  1    0
1 0 1 |  0    1
1 1 0 |  0    1
1 1 1 |  1    1
```

With three outputs, are calculations grow exponentially, but the same theory remains.

```
a b c | sum carry
------|----------
0 0 0 |  0    0
0 0 1 |  1    0 --> NOT(a) AND NOT(b) AND c
0 1 0 |  1    0 --> NOT(a) AND b AND NOT(c)
0 1 1 |  0    1
1 0 0 |  1    0 --> a AND NOT(b) AND NOT(c)
1 0 1 |  0    1
1 1 0 |  0    1
1 1 1 |  1    1 --> a AND b AND c
```

Which equates to the rather long..

```
sum = (NOT(a) AND NOT(b) AND c) OR (NOT(a) AND b AND NOT(c))
OR (a AND NOT(b) AND NOT(c)) OR (a AND b AND c)
```

And can be shortened to.

```
(a XOR b) XOR c
```

#### Negative Numbers

How do you represent negative numbers in binary?

```
0001 = 1
0010 = 2
0011 = 3
```

Let's try dividing the number of possible values by half; one half being positive and the other negative.

```
0110 = 6
0111 = 7
1000 = -0
1001 = -1
```

The first bit in this 4-bit number not acts as a switch; when it is 1 the following three bits represent a negative number, otherwise it is positive.

But that means we've got 2 zeroes; one positive and the other negative.

```
0000 = 0
1000 = -0
```

What is negative zero?

Instead, we can represent negative x like this.

```
2^n - x
```

Where `n` is the number of bits you are using, such as 4. For example, the number -5 is represented by `16 - 5` which is `11`.

```
0101 = 5
1011 = -5
```

This representation is called 2's complement.

And this works wonderfully with subtraction.

```
  -2      14      1110
+ -3    + 13    + 1101
----    ----    ------
  -5      11     11011
                 ^ overflow
```

Here are three identical operations. -2 in 2's complement is 14 (i.e. 16-2) and -3 is 13. Adding those two together results in 27, but 27 is too large to fit in 4-bits, so we throw away the most significant bit, a value of 16, resulting in 11. The same applies to addition using binary. And here's the magical part, 11 just so happens to represent -5 in 2's complement (i.e. 16-5)!

Because we already know addition, subtraction is a matter of converting a negative number into the 2's complement equivalent, and adding it like usual.

```
   7        7       0111
+ -5 --> + 11 --> + 1011
----     ----     ------
   2       18      10010  --> 0010 --> 2
```

How do you actually compute the 2's complement of a number? For example, the number -4, which is 12 (16-4)?

The formula is.

```
2^n - x
```

Which can be rewritten as:

```
1 + (2^n - 1) - x
```

Which is nice, because (2^n - 1) is all 1's. For example, the number 15 of a 4-bit number is `1111`, or the number 7 of a 3-bit number is `111`.

```
  1111
+ 0010
```

.. I still don't understand how to get -x from x..

#### The ALU

```
     zx nx zy ny f no
      |  |  |  | | |
     _v__v__v__v_v_v_
     \               \
x --->|              |
      |              |----> out
y --->|              |
     /_______________/
         |    |
         v    v
        zr    ng

# Control bits
# Input bits metadata
zx = zero out x
nx = NOT(x)
zy = zero out y
ny = NOT(y)
f  = (x + y) if f else (x & y)
no = NOT(out)

# Output bits metadata
zr = 0 if out == 0 else 1
ng = 1 if out < 0 else 1

```

The ALU is the combination of most gates and a few specialised ones.

```
zx | nx | zy | ny | f | no | out
---|----|----|----|---|----|----
 1 | 0  |  1 |  0 | 1 |  0 |  0
 1 | 1  |  1 |  1 | 1 |  1 |  1
 1 | 1  |  1 |  1 | 1 |  1 |  1
 1 | 1  |  1 |  0 | 1 |  0 | -1
 0 | 0  |  1 |  1 | 0 |  0 |  x
 1 | 1  |  0 |  0 | 0 |  0 |  y
 0 | 0  |  1 |  1 | 0 |  1 | !x
 1 | 1  |  0 |  0 | 0 |  1 | !y
 0 | 0  |  1 |  1 | 1 |  1 | -x
 1 | 1  |  0 |  0 | 1 |  1 | -y
 0 | 1  |  1 |  1 | 1 |  1 | x+1
 1 | 1  |  0 |  1 | 1 |  1 | y+1
 0 | 0  |  1 |  1 | 1 |  0 | x-1
 1 | 1  |  0 |  0 | 1 |  0 | y-1
 0 | 0  |  0 |  0 | 1 |  0 | x+y
 0 | 0  |  0 |  1 | 1 |  1 | y-x
 0 | 0  |  0 |  0 | 0 |  0 | x&y
 0 | 1  |  0 |  1 | 0 |  1 | x|y
```