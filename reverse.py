'''
dpcm-reverse - A tool to reverse the bit order of NES DPCM samples
Copyright (C) 2021-present  Kyle Alexander Buan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

print("DPCM sample reverse tool")
print("This tool reverses the bit order of the samples in a NES ROM or NSF.")

rom_path = input("ROM path: ")
a1 = input("Start address in hex (ROM): ")
a2 = input("End address (inclusive) in hex (ROM): ")

if a1.startswith("0x"):
    a1 = a1[2:]
if a2.startswith("0x"):
    a2 = a2[2:]

a_length = int(a2, 16) - int(a1, 16)

print("Length is " + str(a_length) + " bytes.")

print("Opening ROM...")
with open(rom_path, "rb+") as rom:
    print("Seeking to address...")
    rom.seek(int(a1, 16))

    print("Reversing bytes...")
    for a in range(a_length):
        b = rom.read(1)
        b = int.from_bytes(b, byteorder="little", signed=False)
        b = int('{:08b}'.format(b)[::-1], 2)
        rom.seek(-1, 1)
        rom.write(b.to_bytes(1, byteorder="little", signed=False))

print("Done.")