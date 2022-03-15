import yaml


with open(r'.\data\config.yaml') as f:
    CONFIG = yaml.safe_load(f)

if CONFIG['staff']['notes']['note_diameter'] == 'auto':
    CONFIG['staff']['notes']['note_diameter'] = CONFIG['staff']['bars']['inter_bar_distance']

if CONFIG['staff']['notes']['note_margin'] == 'auto':
    CONFIG['staff']['notes']['note_margin'] = CONFIG['staff']['notes']['note_diameter'] / 2

if CONFIG['staff']['bars']['support_bar_length'] == 'auto':
    CONFIG['staff']['bars']['support_bar_length'] = CONFIG['staff']['notes']['note_diameter'] * 2.5
