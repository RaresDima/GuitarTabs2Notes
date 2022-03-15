import yaml


with open(r'.\data\config.yaml') as f:
    CONFIG = yaml.safe_load(f)

CONFIG['staff']['paths'] = {'treble_clef': '.\\data\\img\\treble_clef.svg',
                            'bass_clef': '.\\data\\img\\bass_clef.svg'}

if CONFIG['staff']['notes']['note_width'] == 'auto':
    CONFIG['staff']['notes']['note_width'] = CONFIG['staff']['bars']['inter_bar_distance'] * 1.25

if CONFIG['staff']['notes']['note_margin'] == 'auto':
    CONFIG['staff']['notes']['note_margin'] = CONFIG['staff']['notes']['note_width'] / 2

if CONFIG['staff']['bars']['support_bar_length'] == 'auto':
    CONFIG['staff']['bars']['support_bar_length'] = CONFIG['staff']['notes']['note_width'] * 2.5
