import os

import reportlab
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from svglib.svglib import svg2rlg

import warning
from config import CONFIG
from tab_convertor import GuitarTabConvertor



TAB_FILE = r'.\tabs\guitar\Genshin Impact - Main Theme.txt'

with open(TAB_FILE) as f:
    tab = f.read()

convertor = GuitarTabConvertor(tab)

file_name = os.path.split(TAB_FILE)[1]
title = os.path.splitext(file_name)[0]
tab = convertor.pretty_output_tab(title=title)

with open(os.path.join(CONFIG['output_dir'], file_name), 'w') as f:
    f.write(tab)

print(tab)
print(convertor.raw_output_symbols())

# ---------------------------------


def scale_svg_to_height(svg: Drawing, target_height: int):
    current_height = svg.height
    scale = target_height / current_height

    svg.width = svg.minWidth() * scale
    svg.height = target_height

    svg.scale(scale, scale)
    return svg


def create_staff(pdf: canvas.Canvas,
                 top_left_x: int,
                 top_left_y: int,
                 n_notes: int) -> int:

    inter_bar_distance = CONFIG['staff']['bars']['inter_bar_distance']
    staff_height = inter_bar_distance * 4

    note_width = CONFIG['staff']['notes']['note_diameter'] + 2 * CONFIG['staff']['notes']['note_margin']
    staff_length = note_width * n_notes

    bar_width = CONFIG['staff']['bars']['bar_width']
    bar_transparency = CONFIG['staff']['bars']['bar_transparency']

    right_margin = CONFIG['margins']['right']

    pdf_width, pdf_height = pdf._pagesize

    if top_left_x + staff_length + right_margin > pdf_width:
        max_notes = round((pdf_width - right_margin - top_left_x) // note_width)
        msg = (f'A system with {n_notes} notes (or spaces) would cause the system to go beyond the right margin of the page.\n'
               f'With the current margins and note size you can have {max_notes} (or spaces) on a single system.'
               f'The generated PDF will not look pretty, but it may be usable.\n'
               f'To make the PDF pretty you can try to either:\n'
               f'  - shrink the margins of the page\n'
               f'  - make the notes or note margins smaller\n'
               f'  - manually edit the tabs given as input and split the larger systems into more than 1 system')
        warning.warn(msg)

    pdf.setLineWidth(bar_width)
    pdf.setStrokeColorRGB(0, 0, 0, bar_transparency)

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

    treble_clef_path = CONFIG['staff']['paths']['treble_clef']
    treble_clef_svg = svg2rlg(treble_clef_path)

    treble_clef_height = staff_height + 3 * inter_bar_distance
    treble_clef_svg = scale_svg_to_height(treble_clef_svg, treble_clef_height)

    treble_clef_x = top_left_x
    treble_clef_y = top_left_y - 5.75 * inter_bar_distance
    renderPDF.draw(treble_clef_svg, pdf, treble_clef_x, treble_clef_y)

    draw_grand_staff = CONFIG['staff']['draw_grand_staff']

    if not draw_grand_staff:
        return top_left_y - 4 * inter_bar_distance

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

    return top_left_y - 10 * inter_bar_distance



left_margin = CONFIG['margins']['left']
top_margin  = CONFIG['margins']['top']

inter_staff_distance = CONFIG['staff']['inter_staff_distance']

pdf = canvas.Canvas(os.path.join(CONFIG['output_dir'], title + '.pdf'), pagesize=pagesizes.A4)

width, height = pagesizes.A4

top_left_x = 0
top_left_y = height

current_staff_top_left_x = top_left_x + left_margin
current_staff_top_left_y = top_left_y - top_margin

end_y = create_staff(pdf, current_staff_top_left_x, current_staff_top_left_y, 50)
current_staff_top_left_y = end_y - inter_staff_distance

end_y = create_staff(pdf, current_staff_top_left_x, current_staff_top_left_y, 40)
current_staff_top_left_y = end_y - inter_staff_distance

end_y = create_staff(pdf, current_staff_top_left_x, current_staff_top_left_y, 40)
current_staff_top_left_y = end_y - inter_staff_distance

end_y = create_staff(pdf, current_staff_top_left_x, current_staff_top_left_y, 40)
current_staff_top_left_y = end_y - inter_staff_distance

pdf.save()






