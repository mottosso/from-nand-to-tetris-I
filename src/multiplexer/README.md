### Multiplexer / Demultiplexer

Interleave 2 inputs, and deinterleave them again.

A [multiplexer](https://en.wikipedia.org/wiki/Multiplexer) was a very fascinating concept answering a question I had yet to ask; how do you transmit multiple "channels" of information in a single stream of data, such as wireless networks, or just networks in general?

This is my ad-hoc implementation based on a shallow understanding from reading Wikipedia.

**Building**

```bash
git clone https://github.com/mottosso/from-nand-to-tetris-I.git fntt1
cd fntt1/src/multiplexer
mkdir build
cd build
cmake ..
make
```

**Usage**

```bash
$ echo hello bob  | ./mux | ./demux
hello
bob
```
