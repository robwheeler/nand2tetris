#!/usr/bin/env python3

import re
import sys

class Assembler(object):
  label_pat = re.compile(r'^\(([A-Za-z0-9_.$]*)\)$')
  a_symbol_pat = re.compile(r'^@([A-Za-z][A-Za-z0-9_.$]*)$')
  a_pat = re.compile(r'^@([0-9]*)$')
  dest_pat = re.compile(r'\(([AMD]+=)?\)')
  jump_pat = re.compile(r'\((;(JGT|JEQ|JGE|JLT|JNE|JLE|JMP))?\)')
  def __init__(self):
    self.label_table = {}
    self.variable_table = {
      'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
      'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
      'SCREEN': 16384, 'KBD': 24576,
      'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
    }
    self.jump_table = {
      '':    0, 'JGT': 1, 'JEQ': 2, 'JGE': 3,
      'JLT': 4, 'JNE': 5, 'JLE': 6, 'JMP': 7,
    }
    self.comp_table = {
        '0':42,
        '1': 63,
        '-1': 58,
        'D': 12,
        'A': 48, 'M': 112,
        '!D': 13,
        '!A': 49, '!M': 113,
        '-D': 15,
        '-A': 51, '-M': 115,
        'D+1': 31,
        'A+1': 55, 'M+1': 119,
        'D-1': 14,
        'A-1': 50, 'M-1': 114,
        'D+A': 2, 'D+M': 66,
        'D-A': 19, 'D-M': 83,
        'A-D': 7, 'M-D': 71,
        'D&A': 0, 'D&M': 64,
        'D|A': 21, 'D|M': 85,
    }
    self.instr_strs = []

  def ParseFile(self, filename):
    pc = 0
    for line in open(filename):
      i = line.find('//')
      line = line[:i] if line != -1 else line
      line = line.strip()
      if line:
        m = self.label_pat.match(line)
        if m:
          label = m.groups()[0]
          self.label_table[label] = pc
        else:
          self.instr_strs.append(line)
          pc += 1


  def ReplaceSymbols(self):
    free = 16
    for i, instr in enumerate(self.instr_strs):
      m = self.a_symbol_pat.match(instr)
      if m:
        symbol = m.groups()[0]
        if symbol in self.label_table:
          self.instr_strs[i] = f'@{self.label_table[symbol]}'
        elif symbol in self.variable_table:
          self.instr_strs[i] = f'@{self.variable_table[symbol]}'
        else:
          self.variable_table[symbol] = free
          free += 1
          self.instr_strs[i] = f'@{self.variable_table[symbol]}'

  def OutputBinary(self):
    for instr in self.instr_strs:
      #print(instr)
      m = self.a_pat.match(instr)
      if m:
        print(f'{int(m.groups()[0]):016b}')
      else:
          dest_idx = instr.find('=')
          dest_str = instr[0:dest_idx+1] if dest_idx != -1 else ''
          dest = 0
          if 'M' in dest_str: dest += 1
          if 'D' in dest_str: dest += 2
          if 'A' in dest_str: dest += 4

          jump_idx = instr.find(';')
          jump_str = instr[jump_idx:] if jump_idx != -1 else ''
          jump = self.jump_table[jump_str[1:]]

          comp_str = instr[len(dest_str): jump_idx] if jump_idx != -1 else instr[len(dest_str):]
          #print(f'dest={dest_str}, comp_str={comp_str}, jump_str={jump_str}')
          comp = self.comp_table[comp_str]
          print(f'111{comp:07b}{dest:03b}{jump:03b}')

def main(argv):
  asm = Assembler()
  asm.ParseFile(argv[1])
  asm.ReplaceSymbols()
  asm.OutputBinary()

if __name__ == '__main__':
  main(sys.argv)
