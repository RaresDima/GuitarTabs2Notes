from enum import Enum
from functools import lru_cache
from collections import deque

import warning

from typing import *


class Note:

    class Value(Enum):
        C = 'C'
        Cs = 'C#'
        D = 'D'
        Ds = 'D#'
        E = 'E'
        F = 'F'
        Fs = 'F#'
        G = 'G'
        Gs = 'G#'
        A = 'A'
        As = 'A#'
        B = 'B'

        def __str__(self) -> str:
            return f'Note.Value[{self.value}]'

        __repr__ = __str__

    value: 'Note.Value'
    octave_shift: str

    @staticmethod
    @lru_cache()
    def all_values() -> List['Note.Value']:
        return [Note.Value.C,
                Note.Value.Cs,
                Note.Value.D,
                Note.Value.Ds,
                Note.Value.E,
                Note.Value.F,
                Note.Value.Fs,
                Note.Value.G,
                Note.Value.Gs,
                Note.Value.A,
                Note.Value.As,
                Note.Value.B]

    @staticmethod
    @lru_cache()
    def _next_dict() -> Dict['Note.Value', 'Note.Value']:
        all_values = Note.all_values()
        return dict(zip(all_values, all_values[1:] + [all_values[0]]))

    def __init__(self, value: Union['Note.Value', str], octave_shift: int = 0):
        if isinstance(value, str):
            try:
                self.value = Note.Value(value)
            except ValueError:
                self.value = value
        else:
            self.value = value
        self.octave_shift = octave_shift

    def copy(self) -> 'Note':
        return Note(self.value, self.octave_shift)

    def note_str(self) -> str:
        octave_shift_symbol = ',' if self.octave_shift < 0 else "'"
        octave_shift_count = abs(self.octave_shift)
        return f'{self.value.value}{octave_shift_symbol * octave_shift_count}'

    def __str__(self) -> str:
        return f'Note[{self.note_str()}]'

    __repr__ = __str__

    def __iadd__(self, semitones: int) -> 'Note':
        if semitones == 0:
            pass

        if semitones > 0:
            notes = self.all_values()
            curr_note_pos = notes.index(self.value)
            notes_left = len(notes) - curr_note_pos - 1
            if semitones <= notes_left:
                self.value = notes[curr_note_pos + semitones]
            else:  # semitones > notes_left
                self.octave_shift += (semitones - notes_left) // len(notes) + 1
                self.value = notes[(semitones - notes_left) % len(notes) - 1]

        if semitones < 0:
            semitones = abs(semitones)
            notes = self.all_values()
            curr_note_pos = notes.index(self.value)
            notes_left = curr_note_pos
            if semitones <= notes_left:
                self.value = notes[curr_note_pos - semitones]
            else:  # semitones > notes_left
                self.octave_shift -= (semitones - notes_left) // len(notes) + 1
                self.value = notes[-((semitones - notes_left) % len(notes))]

        return self

    def __add__(self, semitones: int) -> 'Note':
        result = self.copy()
        result += semitones
        return result

    def __isub__(self, semitones: int) -> 'Note':
        return self.__iadd__(-semitones)

    def __sub__(self, semitones: int) -> 'Note':
        return self.__add__(-semitones)

    def __eq__(self, other: 'Note') -> bool:
        return (type(self) == type(other) and
                self.value == other.value and
                self.octave_shift == other.octave_shift)

    def __gt__(self, other: 'Note') -> bool:
        if self.octave_shift > other.octave_shift:
            return True

        if self.octave_shift < other.octave_shift:
            return False

        if self.octave_shift == other.octave_shift:
            notes = self.all_values()
            self_note_pos = notes.index(self.value)
            other_note_pos = notes.index(other.value)
            return self_note_pos > other_note_pos

    def __lt__(self, other: 'Note') -> bool:
        if self.octave_shift < other.octave_shift:
            return True

        if self.octave_shift > other.octave_shift:
            return False

        if self.octave_shift == other.octave_shift:
            notes = self.all_values()
            self_note_pos = notes.index(self.value)
            other_note_pos = notes.index(other.value)
            return self_note_pos < other_note_pos

    def __ge__(self, other: 'Note') -> bool:
        return self > other or self == other

    def __le__(self, other: 'Note') -> bool:
        return self < other or self == other

    def make_higher_than(self, other: 'Note') -> 'Note':
        while self <= other:
            self.octave_shift += 1
        return self

    def make_lower_than(self, other: 'Note') -> 'Note':
        while self >= other:
            self.octave_shift -= 1
        return self


class GuitarTabConvertor:
    raw_tab: str
    tab: str
    tuning: List[Note]

    _active_tab: List[Deque[str]]
    _active_output: List[Union[str, Note]]

    def __init__(self, raw_tab: str):
        self.raw_tab = raw_tab
        self.tuning, self.tab = GuitarTabConvertor._process_raw_tab(self.raw_tab)
        self._active_tab = [deque(line) for line in self.tab]

        self._active_output = []
        while not all(len(line) == 0 for line in self._active_tab):
            current_symbol = self._process_next_symbol()
            self._active_output += [current_symbol]

    @staticmethod
    def _process_raw_tab(raw_tab: str) -> Tuple[List[Note], str]:

        tabs = raw_tab.strip().split('\n\n')

        tab = tabs[0].upper().strip().split('\n')
        tuning = [Note(line.partition('|')[0]) for line in tab[::-1]]
        for i in range(1, len(tuning)):
            tuning[i].make_higher_than(tuning[i - 1])  # bottom to top

        tabs = [tab.strip().split('\n') for tab in tabs]

        tabs = [[line.partition('|')[2]
                 for line in tab]
                for tab in tabs]

        tabs = list(zip(*tabs))

        tabs = [''.join(('|',) + line) for line in tabs]

        # print(*tabs, sep='\n')
        # print(*tuning[::-1], sep='\n')

        return tuning[::-1], tabs

    def _process_next_symbol(self) -> str:
        current_symbols = [line.popleft() for line in self._active_tab]

        set_of_current_symbols = set(current_symbols)

        if set_of_current_symbols == {'-'}:  # all are '-'
            # pause / nothing
            return '-'

        if set_of_current_symbols == {'|'}:  # all are '-'
            # pause / nothing
            return '|'

        if len(set_of_current_symbols) == 2:
            set_of_current_symbols.remove('-')
            current_symbol = list(set_of_current_symbols)[0]
            current_string_pos = current_symbols.index(current_symbol)
            current_string = self._active_tab[current_string_pos]

            current_symbol = list(current_symbol)
            while current_string[0] not in {'-', '|'}:
                current_symbol += [current_string.popleft()]

            if len(current_symbol) > 1:
                msg = f'Unknown symbol encountered: "{"".join(current_symbol)}".'
                current_symbol = [c for c in current_symbol
                                  if c in {'0', '1', '2', '3', '4', '5', '6', '7', '8',  '9'}]
                if current_symbol:
                    msg += f' Extracted symbol {current_symbol}'
                    warning.warn(msg)
                else:
                    msg += f' No number found.'
                    raise ValueError(msg)

            current_fret = int(''.join(current_symbol))
            current_string_base_note = self.tuning[current_string_pos]
            current_note = current_string_base_note + current_fret

            return current_note

        raise ValueError(f'Found unknown set of current symbols: {set_of_current_symbols}')

    def raw_output_symbols(self) -> List[Union[str, Note]]:
        return self._active_output

    def raw_output_symbols_by_system(self) -> List[List[Union[str, Note]]]:
        output = self._active_output.copy()
        bar_locations = [i for i, symbol in enumerate(output) if symbol == '|']
        systems = []
        for system_start, system_end in zip(bar_locations[:-1], bar_locations[1:]):
            systems += [output[system_start+1:system_end]]
        return systems

    def raw_output_tab(self) -> str:
        return ''.join([(symbol.note_str() if isinstance(symbol, Note) else symbol)
                        for symbol in self._active_output])

    def pretty_output_tab(self, title: str = None) -> str:
        output = ''.join(['|', self.raw_output_tab().strip().strip('|').replace('|', '|\n\n|'), '|\n'])
        if title:
            output = '\n\n'.join([title, output])
        return output

