import os
import sys

import reportlab
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts
from svglib.svglib import svg2rlg

import warning
from config import CONFIG
from tab_convertor import Note
from tab_convertor import GuitarTabConvertor

from tkinter import Tk
from tkinter.filedialog import askopenfilename

from typing import *


# make all relative paths be relative to the root dir of the program

os.chdir(os.path.split(sys.argv[0])[0])

# get the tab file, read it, convert it, output the plaintext result

Tk().withdraw()
tab_file = askopenfilename(title='Select a file containing guitar tabs', initialdir=os.getcwd())
# tab_file = r'E:\Tools\Projects\PyCharm Projects\GuitarTabs2Notes\tabs\guitar\Genshin Impact - Main Theme.txt'

with open(tab_file) as f:
    tab = f.read()

convertor = GuitarTabConvertor(tab)

file_name = os.path.split(tab_file)[1]
title = os.path.splitext(file_name)[0]
tab = convertor.pretty_output_tab(title=title)

if not os.path.isdir(CONFIG['output_dir']):
    os.makedirs(CONFIG['output_dir'], exist_ok=True)

with open(os.path.join(CONFIG['output_dir'], file_name), 'w') as f:
    f.write(tab)

# create the pretty pdf


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

    note_block_width = CONFIG['staff']['notes']['note_width'] + 2 * CONFIG['staff']['notes']['note_margin']
    note_blocks_length = note_block_width * n_notes

    bar_width = CONFIG['staff']['bars']['bar_width']
    bar_transparency = CONFIG['staff']['bars']['bar_transparency']

    pdf.setLineWidth(bar_width)
    pdf.setStrokeColorRGB(0, 0, 0, bar_transparency)

    # treble clef setup

    treble_clef_path = CONFIG['paths']['treble_clef_svg']
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
               f'With the current margins and note size you can have {max_notes} notes (or spaces) on a single system. '
               f'The generated PDF will not look pretty, but it *may* be usable.\n'
               f'To make the PDF pretty you can try to make some changes before re-running the program:\n'
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

    bass_clef_path = CONFIG['paths']['bass_clef_svg']
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
        'F' : +0,
        'F#': +0,
        'G' : +1,
        'G#': +1,
        'A' : +2,
        'A#': +2,
        'B' : +3
    }
    base_diff = base_diffs_from_f[note.value.value]
    octave_shift = note.octave_shift - 1
    diff = base_diff + octave_shift * 7
    return diff


def add_note_to_system(pdf: canvas.Canvas,
                       note: Note,
                       position: int,
                       first_block_left_x: int,
                       top_bar_y: int, ):

    pdf.setStrokeColorRGB(0, 0, 0, 1.0)
    pdf.setFillColorRGB(0, 0, 0, 1.0)

    inter_bar_distance = CONFIG['staff']['bars']['inter_bar_distance']
    bar_width = CONFIG['staff']['bars']['bar_width']
    note_width = CONFIG['staff']['notes']['note_width']
    note_margin = CONFIG['staff']['notes']['note_margin']

    block_width = note_margin + note_width + note_margin
    target_block_start_x = first_block_left_x + position * block_width
    note_center_x = target_block_start_x + block_width / 2

    semibar_diff = semibars_relative_to_center_of_top_bar(note)
    note_y_offset = semibar_diff * (inter_bar_distance / 2)
    note_center_y = top_bar_y + note_y_offset

    if semibar_diff > +0 or semibar_diff < -8:

        bar_transparency = CONFIG['staff']['bars']['bar_transparency']
        support_bar_length = CONFIG['staff']['bars']['support_bar_length']

        pdf.setLineWidth(bar_width)
        pdf.setStrokeColorRGB(0, 0, 0, bar_transparency)

        line_start_x = note_center_x - 0.5 * support_bar_length
        line_end_x = note_center_x + 0.5 * support_bar_length

        current_diff = semibar_diff
        diff_shift_factor = -2 if semibar_diff > 0 else +2
        line_y_shift_factor = (-1 if semibar_diff > 0 else +1) * inter_bar_distance

        if semibar_diff % 2 == 0:  # bar trough
            line_y = note_center_y

        elif semibar_diff >= +1:  # bar under
            line_y = note_center_y - inter_bar_distance / 2

        elif semibar_diff <= -9:  # bar over
            line_y = note_center_y + inter_bar_distance / 2

        while current_diff > +1 or current_diff < -9:
            pdf.line(line_start_x, line_y, line_end_x, line_y)
            current_diff += diff_shift_factor
            line_y += line_y_shift_factor

    # pdf.circle(note_center_x, note_center_y, note_width/2, stroke=0, fill=1)
    note_left_x = note_center_x - note_width / 2
    note_right_x = note_center_x + note_width / 2
    note_bottom_y = note_center_y - inter_bar_distance / 2 + bar_width / 2
    note_top_y = note_center_y + inter_bar_distance / 2 - bar_width / 2

    pdf.ellipse(note_left_x, note_bottom_y, note_right_x, note_top_y, stroke=0, fill=1)

    # note label

    draw_note_labels = CONFIG['staff']['notes']['labels']['draw_labels']

    if not draw_note_labels:
        return

    note_height = note_top_y - note_bottom_y
    note_label_height = note_height * 0.75
    note_label_bottom_y = note_center_y - note_label_height / 2.5

    note_label_text = note.value.value
    note_label_font = CONFIG['staff']['notes']['labels']['font']
    pdf.setFont(note_label_font, note_label_height)
    note_label_width = pdfmetrics.stringWidth(note_label_text, note_label_font, note_label_height)
    note_label_left_x = note_center_x - note_label_width / 2

    pdf.setFillColorRGB(1, 1, 1)
    pdf.drawString(note_label_left_x, note_label_bottom_y, note_label_text)


def add_notes_to_system(pdf: canvas.Canvas,
                        notes: List[Note],
                        first_block_left_x: int,
                        top_bar_y: int):

    for pos, symbol in enumerate(notes):
        if symbol == '-':
            continue

        add_note_to_system(pdf, symbol, pos, first_block_left_x, top_bar_y)


# config values

left_margin = CONFIG['margins']['left']
top_margin  = CONFIG['margins']['top']
bottom_margin = CONFIG['margins']['bottom']

inter_staff_distance = CONFIG['staff']['inter_staff_distance']
inter_bar_distance = CONFIG['staff']['bars']['inter_bar_distance']
staff_height = inter_bar_distance * 4

font_dir = CONFIG['paths']['font_dir']
for file in os.listdir(font_dir):
    file_name, file_type = os.path.splitext(file)
    if file_type.lower() == '.ttf':  # is font file
        font_name = file_name
        font_path = os.path.join(font_dir, file)
        font = ttfonts.TTFont(font_name, font_path)
        pdfmetrics.registerFont(font)

# create the pdf

pdf = canvas.Canvas(os.path.join(CONFIG['output_dir'], title + '.pdf'), pagesize=pagesizes.A4)

# setup starting coords

width, height = pagesizes.A4

top_left_x = 0
top_left_y = height

current_staff_top_left_x = top_left_x + left_margin
current_staff_top_left_y = top_left_y - top_margin

# add title

draw_title = CONFIG['title']['draw_title']

if draw_title:
    title_height = CONFIG['title']['font_size']
    title_font = CONFIG['title']['font']
    title_top_margin = CONFIG['title']['margins']['top']
    title_bottom_margin = CONFIG['title']['margins']['bottom']
    pdf.setFont(title_font, title_height)
    title_width = pdfmetrics.stringWidth(title, title_font, title_height)
    title_left_x = width / 2 - title_width / 2
    title_bottom_y = current_staff_top_left_y - title_height - title_top_margin
    pdf.drawString(title_left_x, title_bottom_y, title)

    current_staff_top_left_y = title_bottom_y - title_bottom_margin

# add staves and notes

for system in convertor.raw_output_symbols_by_system():
    first_block_left_x, bottom_bar_y = create_staff(pdf, len(system), current_staff_top_left_x, current_staff_top_left_y)
    add_notes_to_system(pdf, system, first_block_left_x, current_staff_top_left_y)
    current_staff_top_left_y = bottom_bar_y - inter_staff_distance

    # should we go to next page?

    space_left = current_staff_top_left_y
    space_needed = staff_height + max(inter_staff_distance, bottom_margin)
    if space_left < space_needed:
        pdf.showPage()
        current_staff_top_left_x = top_left_x + left_margin
        current_staff_top_left_y = top_left_y - top_margin

first_block_left_x, bottom_bar_y = create_staff(pdf, 30, current_staff_top_left_x, current_staff_top_left_y)
current_staff_top_left_y = bottom_bar_y - inter_staff_distance

pdf.save()

print('Done!')
print(f'Output files created in: {os.path.abspath(CONFIG["output_dir"])}')
input('Press Enter to end the program...')
