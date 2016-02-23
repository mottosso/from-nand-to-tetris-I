// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@R2 // Initialize to zero
	M=0

	// If either multiplicand or multiplier is zero
	@R0
	D=M

	@END
	D;JEQ // Jump if D == 0

	@R1
	D=M

	@END
	D;JEQ

	// Start loop
	D=0

(LOOP)
	// Add R0 to current result
	@R2
	D=M

	@R0
	D=D+M

	// Update result
	@R2
	M=D

	// Consider next multiplier
	@R1
	M=M-1
	D=M

	@LOOP
	D;JNE

(END)
	@END
	0;JMP