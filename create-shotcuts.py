from subprocess import call

# Change to match mate-grid installation path
mate_grid_path = '/opt/mate-grid/mate-grid.py'

shortcuts = {
    'mate-grid-move-next-mon': {
        'name': 'Move window to next Monitor', 
        'action': 'python {} -cm'.format(mate_grid_path),
        'binding': '<Shift><Mod4>Right'
    },
    'mate-grid-move-prev-mon': {
        'name': 'Move window to previous Monitor', 
        'action': 'python {} -cm'.format(mate_grid_path),
        'binding': '<Shift><Mod4>Left'
    },
    'mate-grid-move-left': {
        'name': "Move window to the left half",
        'action': 'python {} -ml'.format(mate_grid_path),
        'binding': '<Mod4>Left'
    },
    'mate-grid-move-right': {
        'name': "Move window to the left half",
        'action': 'python {} -mr'.format(mate_grid_path),
        'binding': '<Mod4>Right'
    },
    'mate-grid-move-top': {
        'name': "Move window to the top half",
        'action': 'python {} -mt'.format(mate_grid_path),
        'binding': '<Ctrl><Mod4>Up'
    },
    'mate-grid-move-bottom': {
        'name': "Move window to the bottom half",
        'action': 'python {} -mb'.format(mate_grid_path),
        'binding': '<Ctrl><Mod4>Down'
    },
    'mate-grid-move-top-left': {
        'name': "Move window to the top left quarter",
        'action': 'python {} -mtl'.format(mate_grid_path),
        'binding': '<Shift><Ctrl><Mod4>Up'
    },
    'mate-grid-move-top-right': {
        'name': "Move window to the top right quarter",
        'action': 'python {} -mtr'.format(mate_grid_path),
        'binding': '<Shift><Ctrl><Mod4>Right'
    },
    'mate-grid-move-bottom-left': {
        'name': "Move window to the bottom left quarter",
        'action': 'python {} -mbl'.format(mate_grid_path),
        'binding': '<Shift><Ctrl><Mod4>Left'
    },
    'mate-grid-move-bottom-right': {
        'name': "Move window to the bottom right quarter",
        'action': 'python {} -mbr'.format(mate_grid_path),
        'binding': '<Shift><Ctrl><Mod4>Down'
    }
}

for key_container, params in shortcuts.iteritems():
    for key, value in params.iteritems():
        command = ['gsettings', 'set',
            'org.mate.control-center.keybinding:/org/mate/desktop/keybindings/{}/'.format(key_container),
            key,
            '"{}"'.format(value)
        ]
        call (command)
        # Debug.
        #print " ".join(command)
