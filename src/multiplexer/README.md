### Multiplexer / Demultiplexer

Interleave 2 inputs, and deinterleave them again.

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
