import yaml


with open(r'.\data\config.yaml') as f:
    CONFIG = yaml.safe_load(f)


CONFIG['paths'] = {'treble_clef_svg': '.\\data\\img\\treble_clef.svg',
                   'bass_clef_svg': '.\\data\\img\\bass_clef.svg',
                   'font_dir': '.\\data\\fonts'}

# ---

if CONFIG['staff']['notes']['note_width'] == 'auto':
    CONFIG['staff']['notes']['note_width'] = CONFIG['staff']['bars']['inter_bar_distance'] * 1.25

if CONFIG['staff']['notes']['note_margin'] == 'auto':
    CONFIG['staff']['notes']['note_margin'] = CONFIG['staff']['notes']['note_width'] / 4

if CONFIG['staff']['bars']['support_bar_length'] == 'auto':
    CONFIG['staff']['bars']['support_bar_length'] = CONFIG['staff']['notes']['note_width'] * 2

# ---

if CONFIG['title']['margins']['top'] == 'auto':
    CONFIG['title']['margins']['top'] = CONFIG['staff']['inter_staff_distance'] / 4

if CONFIG['title']['margins']['bottom'] == 'auto':
    CONFIG['title']['margins']['bottom'] = CONFIG['staff']['inter_staff_distance'] * 1.5

# ---

if CONFIG['margins']['bottom'] == 'auto':
    CONFIG['margins']['bottom'] = CONFIG['margins']['top']

if CONFIG['margins']['right'] == 'auto':
    CONFIG['margins']['right'] = CONFIG['margins']['left']
