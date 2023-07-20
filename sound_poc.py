import asyncio
import board
import keypad
import displayio
import framebufferio
import rgbmatrix
import time
import terminalio
import adafruit_display_text.label
import array
import math
import audiocore
import audiobusio

bit_depth_value = 6
unit_width = 64
unit_height = 64
chain_width = 1
chain_height = 1
serpentine_value = True

width_value = unit_width * chain_width
height_value = unit_height * chain_height

displayio.release_displays()


async def beeper():
    audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP15)
    tone_volume = 0.08  # Increase this to increase the volume of the tone.
    sample_rate = 8000

    phrase = "C@C@C@< >A@<C   "  # 5353531 24315
    # phrase = "<>@<C   CEHEC   "  # 12315   56865
    # phrase = "484; "  # The phrase to be spoken
    # phrase = "484;CCC "
    character_duration = int(sample_rate / 4)  # Duration of each character
    silence_duration = int(sample_rate / 16)  # Duration of silence between characters

    # Generate the robot speech
    speech_length = (len(phrase) * character_duration) + ((len(phrase) - 1) * silence_duration)
    robot_speech = array.array("h", [0] * speech_length)

    for i, char in enumerate(phrase):
        char_start = i * (character_duration + silence_duration)
        char_end = char_start + character_duration

        for j in range(char_start, char_end):
            t = (j - char_start) / character_duration  # Time within the current character

            # Generate the speech waveform
            if char == " ":
                robot_speech[j] = 0  # Silence for spaces
            else:
                frequency = 50 + ord(char) * 20  # Modulate frequency based on character
                robot_speech[j] = int(tone_volume * math.sin(2 * math.pi * frequency * t) * (2 ** 15 - 1))

    sine_wave_sample = audiocore.RawSample(robot_speech)

    audio.play(sine_wave_sample, loop=True)
    await asyncio.sleep(6)
    audio.stop()
    await asyncio.sleep(0.1)


async def main():
    beeper_task = asyncio.create_task(beeper())
    await asyncio.gather(
        beeper_task,
    )


asyncio.get_event_loop().run_until_complete(main())
