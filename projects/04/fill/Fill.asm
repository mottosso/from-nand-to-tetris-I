// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.

(RESTART)
	@SCREEN
	D=A

	@addr
	M=D   // addr = 16384
		  // (screen's base address)

	@0
	D=M
	@n
	M=D  // n = RAM[0]

	@i
	M=0  // i = 0

(LOOP)
	@i
	D=M
	@n
	D=D-M

	@KBD
	D=M

	@BLACK
	D;JEQ

(WHITE)
	@addr
	A=M
	M=0
	@DONE
	0;JMP

(BLACK)
	@addr
	A=M
	M=-1  // RAM[addr]=111111...

(DONE)
	@i
	M=M+1 // i++

	@addr
	M=M+1
	D=M

	// Once it hits the end of the screen
	// memory map, reset the counters and
	// start again
	@KBD
	D=A-D

	@RESTART
	D;JEQ

	@LOOP
	0;JMP // goto LOOP

(END)
	@END
	0;JMP