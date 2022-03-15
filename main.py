import os

import reportlab
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from svglib.svglib import svg2rlg

import warning
from config import CONFIG
from tab_convertor import Note
from tab_convertor import GuitarTabConvertor

from typing import *


TAB_FILE = r'.\tabs\guitar\Genshin Impact - Main Theme.txt'

with open(TAB_FILE) as f:
    tab = f.read()

convertor = GuitarTabConvertor(tab)

file_name = os.path.split(TAB_FILE)[1]
title = os.path.splitext(file_name)[0]
tab = convertor.pretty_output_tab(title=title)

with open(os.path.join(CONFIG['output_dir'], file_name), 'w') as f:
    f.write(tab)

# ---------------------------------


def scale_svg_to_height(svg: Drawing, target_height: int):
    current_height = svg.height
    scale = target_height / current_height

    svg.width = svg.minWidth() * scale
    svg.height = target_height

    svg.scale(scale, scale)
    return svg


def create_staff(pdf: canvas.Canvas,
                 n_notes: int,
                 top_left_x: int,
                 top_left_y: int) -> Tuple[int, int]:

    inter_bar_distance = CONFIG['staff']['bars']['inter_bar_distance']
    staff_height = inter_bar_distance * 4

    note_block_width = CONFIG['staff']['notes']['note_diameter'] + 2 * CONFIG['staff']['notes']['note_margin']
    note_blocks_length = note_block_width * n_notes

    bar_width = CONFIG['staff']['bars']['bar_width']
    bar_transparency = CONFIG['staff']['bars']['bar_transparency']

    pdf.setLineWidth(bar_width)
    pdf.setStrokeColorRGB(0, 0, 0, bar_transparency)

    # treble clef setup

    treble_clef_path = CONFIG['staff']['paths']['treble_clef']
    treble_clef_svg = svg2rlg(treble_clef_path)

    treble_clef_height = staff_height + 3 * inter_bar_distance
    treble_clef_svg = scale_svg_to_height(treble_clef_svg, treble_clef_height)
    treble_clef_width = treble_clef_svg.width

    staff_length = treble_clef_width + note_blocks_length

    # treble staff

    pdf.line(top_left_x,
             top_left_y,
             top_left_x,
             top_left_y - staff_height)

    pdf.line(top_left_x,
             top_left_y,
             top_left_x + staff_length,
             top_left_y)

    pdf.line(top_left_x,
             top_left_y - inter_bar_distance,
             top_left_x + staff_length,
             top_left_y - inter_bar_distance)

    pdf.line(top_left_x,
             top_left_y - 2 * inter_bar_distance,
             top_left_x + staff_length,
             top_left_y - 2 * inter_bar_distance)

    pdf.line(top_left_x,
             top_left_y - 3 * inter_bar_distance,
             top_left_x + staff_length,
             top_left_y - 3 * inter_bar_distance)

    pdf.line(top_left_x,
             top_left_y - 4 * inter_bar_distance,
             top_left_x + staff_length,
             top_left_y - 4 * inter_bar_distance)

    pdf.line(top_left_x + staff_length,
             top_left_y,
             top_left_x + staff_length,
             top_left_y - staff_height)


    # treble clef

    treble_clef_x = top_left_x
    treble_clef_y = top_left_y - 5.75 * inter_bar_distance
    renderPDF.draw(treble_clef_svg, pdf, treble_clef_x, treble_clef_y)

    # width warning

    right_margin = CONFIG['margins']['right']
    pdf_width, pdf_height = pdf._pagesize

    if top_left_x + staff_length + right_margin > pdf_width:
        max_notes = round((pdf_width - right_margin - top_left_x - treble_clef_width) // note_block_width)
        msg = (f'A system with {n_notes} notes (or spaces) would cause the system to go beyond the right margin of the page.\n'
               f'With the current margins and note size you can have {max_notes} notes (or spaces) on a single system.'
               f'The generated PDF will not look pretty, but it may be usable.\n'
               f'To make the PDF pretty you can try to either:\n'
               f'  - shrink the margins of the page\n'
               f'  - make the notes or note margins smaller\n'
               f'  - manually edit the tabs given as input and split the larger systems into more than 1 system')
        warning.warn(msg)

    # grand staff decision

    draw_grand_staff = CONFIG['staff']['draw_grand_staff']

    if not draw_grand_staff:
        return (treble_clef_x + treble_clef_width,
                top_left_y - staff_height)

    # bass staff

    pdf.line(top_left_x,
             top_left_y - 6 * inter_bar_distance,
             top_left_x,
             top_left_y - 6 * inter_bar_distance - staff_height)

    pdf.line(top_left_x,
             top_left_y - 6 * inter_bar_distance,
             top_left_x + staff_length,
             top_left_y - 6 * inter_bar_distance)


    pdf.line(top_left_x,
             top_left_y - 7 * inter_bar_distance,
             top_left_x + staff_length,
             top_left_y - 7 * inter_bar_distance)

    pdf.line(top_left_x,
             top_left_y - 8 * inter_bar_distance,
             top_left_x + staff_length,
             top_left_y - 8 * inter_bar_distance)

    pdf.line(top_left_x,
             top_left_y - 9 * inter_bar_distance,
             top_left_x + staff_length,
             top_left_y - 9 * inter_bar_distance)

    pdf.line(top_left_x,
             top_left_y - 10 * inter_bar_distance,
             top_left_x + staff_length,
             top_left_y - 10 * inter_bar_distance)

    pdf.line(top_left_x + staff_length,
             top_left_y - 6 * inter_bar_distance,
             top_left_x + staff_length,
             top_left_y - 6 * inter_bar_distance - staff_height)

    # bass clef

    bass_clef_path = CONFIG['staff']['paths']['bass_clef']
    bass_clef_svg = svg2rlg(bass_clef_path)

    bass_clef_height = 3.25 * inter_bar_distance
    bass_clef_svg = scale_svg_to_height(bass_clef_svg, bass_clef_height)

    treble_clef_width = treble_clef_svg.width
    bass_clef_width = bass_clef_svg.width
    half_width_diff = (treble_clef_width - bass_clef_width) / 2
    half_width_diff_adjusted = half_width_diff * 1.2

    bass_clef_x = top_left_x + half_width_diff_adjusted
    bass_clef_y = top_left_y - 9.25 * inter_bar_distance
    renderPDF.draw(bass_clef_svg, pdf, bass_clef_x, bass_clef_y)

    return (treble_clef_x + treble_clef_width,
            top_left_y - 2 * staff_height - 2 * inter_bar_distance)


def semibars_relative_to_center_of_top_bar(note: Note) -> int:
    base_diffs_from_f = {
        'C' : -3,
        'C#': -3,
        'D' : -2,
        'D#': -2,
        'E' : -1,
        'F' : 0,
        'F#': 0,
        'G' : 1,
        'G#': 1,
        'A' : 2,
        'A#': 2,
        'B' : 3
    }
    # E = E4
    # c#' = C3#
    base_diff = base_diffs_from_f[note.value.value]





def draw_note(note: Note,
              position: int,
              first_block_left_x: int,
              top_bar_y: int,):

    pdf.setStrokeColorRGB(0, 0, 0, 1.0)

    inter_bar_distance = CONFIG['staff']['bars']['inter_bar_distance']

    note_diameter = CONFIG['staff']['notes']['note_diameter']
    note_margin = CONFIG['staff']['notes']['note_margin']

    block_width = note_margin + note_diameter + note_margin

    target_block_start_x = first_block_left_x + position * block_width













left_margin = CONFIG['margins']['left']
top_margin  = CONFIG['margins']['top']

inter_staff_distance = CONFIG['staff']['inter_staff_distance']

pdf = canvas.Canvas(os.path.join(CONFIG['output_dir'], title + '.pdf'), pagesize=pagesizes.A4)

width, height = pagesizes.A4

top_left_x = 0
top_left_y = height

current_staff_top_left_x = top_left_x + left_margin
current_staff_top_left_y = top_left_y - top_margin

for system in convertor.raw_output_symbols_by_system():
    first_block_left_x, bottom_bar_y = create_staff(pdf, len(system), current_staff_top_left_x, current_staff_top_left_y)
    current_staff_top_left_y = bottom_bar_y - inter_staff_distance

first_block_left_x, bottom_bar_y = create_staff(pdf, 30, current_staff_top_left_x, current_staff_top_left_y)
current_staff_top_left_y = bottom_bar_y - inter_staff_distance

pdf.save()

print(*convertor.raw_output_symbols_by_system(), sep='\n')






