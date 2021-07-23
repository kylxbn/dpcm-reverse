# dpcm-reverse

## Overview

This tool was created in order to flip the bit order of DPCM samples
used in NES video games.

## Motivation

Some (or many?) NES games are not aware that the NES audio system plays DPCM samples from least significant to most significant. This is most noticeable with the video game Double Dribble where the voice at the start of the game sounds weird and distorted. It turned out that the audio was stored in the reverse order the NES expects it to be, thus distorting the sound.

This tool was created to reverse the bit order in the ROM itself.

## Usage

Just run the script in Python3 and it should ask you the necessary details one by one.

```sh
python reverse.py
```

| Prompt | What to input |
| ------ | ------------- |
| ROM path | The path to the ROM file you want to patch. This can be relative or absolute. |
| Start address | The start address of the bytes you want to reverse. Note that this will be the actual offset in the ROM file and not the address of the DPCM sample in the NES memory space. You can prefix `0x` or not, it's up to you. |
| End address | The last byte that you want to reverse. Up to this byte will be reversed. The byte after this will not be touched. See the notes for *Start address* for warnings. |

## Testing

I just tested it with Journey to Silius and I think I prefer how it sounds when patched instead of the original. The original is more memorable, but the patched one sounds... cleaner, I guess.

For the NSF file I used, I had to use the following settings:

| Parameter | Value |
| --------- | ----- |
| Start address | 0x4080 |
| End address | 0x5461 |

Yes, the end address is 1 byte over. That's because of a hardware bug of the NES where the specified sample end address is interpreted as that value + 1 byte, so we need to compensate for that.

In order to know what addresses I need to use, I used FCEUX to play the NSF and the built-in *SoundDisplay.lua* script to see the address and length of the currently playing DPCM sample. Fortunately, while *Journey to Silius* uses 5 samples total, they are in contigious bytes, so I don't have to reverse each sample individually, and just treat them as one huge sample.

#### Sample address in NES RAM

| Address | Sample |
| ------- | ------ |
| $C000 | Bass (pitched) |
| $C400 | Bass (pitched) |
| $C800 | Bass (pitched) |
| $CC00 | Bass (pitched) |
| $D000 | Bass (pitched) |

Now, I need to find the address of that in the NSF file. So I went to
FCEUX's built in Hex editor and went to the address I need to see. Right clicking the first byte and selecting "Go Here In ROM File" shows you where that sample is located in the NSF file itself. For example, the first sample at NES RAM `$C000` seems to be located at `0x4010` in the NSF file. However, through trial and error, I realized that FCEUX is showing the wrong file address offset. The real offset is actually `what FCEUX reports + 0x70`, for some weird reason. So there's our start address.

For the end address, I know that the last sample starts at `$D000` but I need to know where it ends. FCEUX's *SoundDisplay.lua* script also shows the sample length in bytes, so just add that (993 bytes) to the start value and we learn that the sample should end at `$D3E1`, so I just need to know where that is in the ROM file using the procedure above and that's all the information we need.

## License

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