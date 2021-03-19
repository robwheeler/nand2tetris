// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(EVENT)
  @KBD
  D=M
  @FILL_BLACK
  D;JNE
  @R0
  M=0
  @FILL
  0;JMP
  (FILL_BLACK)
    @R0
    M=-1
    @FILL
    0;JMP
  @EVENT
  0;JMP

(FILL)
  @16384
  D=A
  @i
  M=D
  (LOOP)
    @i
    D=M
    @24575
    D=D-A
    @EVENT  // while (i < 24576)
    D;JGT

    @R0
    D=M
    @i
    A=M
    M=D

    @i
    M=M+1  // ++i
    @LOOP
    0;JMP
