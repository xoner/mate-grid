from bs4 import BeautifulSoup
from sh import gsettings, xdotool, xwininfo, grep, awk
from os import path
from collections import namedtuple
from argparse import ArgumentParser
from subprocess import call


def get_monitor_config():
    monitorsxml_path = path.expandvars('$HOME/.config/monitors.xml')

    if(not path.exists(monitorsxml_path)):
        print("Error: monitors.xml does not exixsts run monitor config utility\
               from the control pannel")
        return None, None

    monitorsxml = ''
    with open(monitorsxml_path) as monitors_file:
        monitorsxml = monitors_file.read()

    monitors = BeautifulSoup(monitorsxml)

    left_monitor = None
    right_monitor = None

    for monitor in monitors.body.monitors.configuration:
        if hasattr(monitor, 'x') and monitor.x is not None:
            if monitor.x.get_text() == '0':
                left_monitor = monitor
            if monitor.x.get_text() != '0':
                right_monitor = monitor

    monitor_obj = namedtuple('Monitor', ['width', 'height', 'position'])

    left_monitor_obj = monitor_obj(int(left_monitor.width.get_text()),
                                   int(left_monitor.height.get_text()),
                                   int(left_monitor.x.get_text()))
    right_monitor_obj = monitor_obj(int(right_monitor.width.get_text()),
                                    int(right_monitor.height.get_text()),
                                    int(right_monitor.x.get_text()))

    return left_monitor_obj, right_monitor_obj


def get_panel_size():
    panel_size = gsettings("get",
                           "org.mate.panel.toplevel:/org/mate/panel/toplevels/\
                            toplevel_4/",
                           "size")
    return int(panel_size)


def get_window_info():
    window = xdotool('getactivewindow')

    # equivalent to:
    # `xwininfo -id $window | grep "Absolute upper-left X" | awk '{print $4}'`
    position = awk(grep(xwininfo('-id', window), 'Absolute upper-left X'), '{print $4}')
    window_title_offset = awk(grep(xwininfo('-id', window), 'Relative upper-left Y'), '{print $4}')
    window_border_offset = awk(grep(xwininfo('-id', window), 'Relative upper-left X'), '{print $4}')
    # equivalent to `xwininfo -id $window | grep "Width" | awk '{print $2}'`
    width = awk(grep(xwininfo('-id', window), 'Width'), '{print $2}')

    window_obj = namedtuple("Window",
                            ['position',
                             'width',
                             'window_border_offset',
                             'window_title_offset'])

    return window_obj(int(position),
                      int(width),
                      int(window_border_offset),
                      int(window_title_offset))


def get_active_monitor():
    for monitor in monitors_array:
        if current_window.position < monitor.position + monitor.width:
            return monitor


def window_maximized(current_monitor):
    return current_window.width >= current_monitor.width


def remove_maximized_state():
    # wmctrl('-r', ':ACTIVE:','-b', 'remove,maximized_vert,maximized_horz')
    call(['wmctrl',
         '-r', ':ACTIVE:', '-b', 'remove,maximized_vert,maximized_horz'])


def restore_maximized_state():
    # wmctrl('-r', ':ACTIVE:','-b', 'add,maximized_vert,maximized_horz')
    call(['wmctrl',
         '-r', ':ACTIVE:', '-b', 'add,maximized_vert,maximized_horz'])


def get_panel_waste(active_monitor):
    # TODO: really check if the monitor have pannels and calculate the "wasted space"
    panel_wasted = 0
    if active_monitor.position == 0:
        panel_wasted = panel_size

    return panel_wasted


def move_window(mvarg):
    active_monitor = get_active_monitor()

    if window_maximized(active_monitor):
        remove_maximized_state()

    call(['wmctrl', '-r', ':ACTIVE:',
         '-e', '0,{},{},{},{}'.format(*mvarg)])


def move_window_left():
    active_monitor = get_active_monitor()

    position = [
        active_monitor.position,
        0,
        (active_monitor.width / 2) - current_window.window_border_offset * 2,
        active_monitor.height - get_panel_waste(active_monitor)
        ]

    move_window(position)


def move_window_right():
    active_monitor = get_active_monitor()

    position = [
        active_monitor.position + (active_monitor.width / 2),
        0,
        (active_monitor.width / 2) - current_window.window_border_offset * 2,
        active_monitor.height - get_panel_waste(active_monitor)]

    move_window(position)


def move_window_top():
    active_monitor = get_active_monitor()

    position = [
        active_monitor.position,
        0,
        active_monitor.width,
        ((active_monitor.height - get_panel_waste(active_monitor)) / 2) - (current_window.window_title_offset + current_window.window_border_offset)
    ]

    move_window(position)


def move_window_bottom():
    active_monitor = get_active_monitor()

    position = [
        active_monitor.position,
        active_monitor.height / 2,
        active_monitor.width,
        ((active_monitor.height - get_panel_waste(active_monitor)) / 2) - (current_window.window_title_offset + current_window.window_border_offset)

    ]

    move_window(position)


def move_window_top_left():
    active_monitor = get_active_monitor()

    position = [
        active_monitor.position,
        0,
        (active_monitor.width / 2) - current_window.window_border_offset * 2,
        ((active_monitor.height - get_panel_waste(active_monitor)) / 2) - (current_window.window_title_offset + current_window.window_border_offset)
    ]

    move_window(position)


def move_window_top_right():
    active_monitor = get_active_monitor()

    position = [
        active_monitor.position + active_monitor.width / 2,
        0,
        (active_monitor.width / 2) - current_window.window_border_offset * 2,
        ((active_monitor.height - get_panel_waste(active_monitor)) / 2) - (current_window.window_title_offset + current_window.window_border_offset)
    ]

    move_window(position)


def move_window_bottom_left():
    active_monitor = get_active_monitor()

    position = [
        active_monitor.position,
        active_monitor.height / 2,
        (active_monitor.width / 2) - current_window.window_border_offset * 2,
        ((active_monitor.height - get_panel_waste(active_monitor)) / 2) - (current_window.window_title_offset + current_window.window_border_offset)
    ]

    move_window(position)


def move_window_bottom_right():
    active_monitor = get_active_monitor()

    position = [
        active_monitor.position + active_monitor.width / 2,
        active_monitor.height / 2,
        (active_monitor.width / 2) - current_window.window_border_offset * 2,
        ((active_monitor.height - get_panel_waste(active_monitor)) / 2) - (current_window.window_title_offset + current_window.window_border_offset)
    ]

    move_window(position)


def change_monitor():
    # TODO: rewrite to handle more than two monitors

    maximized = False
    nu_position = -1
    # window in left monitor
    if current_window.position < left_monitor.width:
        maximized = window_maximized(left_monitor)

        # check that the window position is still on the visible area of
        # the second monitor if not put the window on top left corner
        nu_position = left_monitor.width + current_window.position
        if nu_position > left_monitor.width + right_monitor.width:
            nu_position = left_monitor.width
    # window in the right monitor.
    else:
        maximized = window_maximized(right_monitor)

        # check if there are something wrong with the new position
        nu_position = current_window.position - left_monitor.width
        if nu_position >= left_monitor.width or nu_position < 0:
            nu_position = 0

    # remove maximized state if maximized.
    if maximized:
        remove_maximized_state()

    call(['wmctrl', '-r', ':ACTIVE:',
          '-e', '0,{},-1,-1,-1'.format(nu_position)])

    # restore maximized state
    if maximized:
        restore_maximized_state()


def main(args):
    if args.move_left:
        move_window_left()
    elif args.move_right:
        move_window_right()
    elif args.move_top:
        move_window_top()
    elif args.move_bottom:
        move_window_bottom()
    elif args.move_top_left:
        move_window_top_left()
    elif args.move_top_right:
        move_window_top_right()
    elif args.move_bottom_left:
        move_window_bottom_left()
    elif args.move_bottom_right:
        move_window_bottom_right()
    elif args.change_monitor:
        change_monitor()


current_window = get_window_info()
left_monitor, right_monitor = get_monitor_config()
monitors_array = [left_monitor, right_monitor]
panel_size = get_panel_size()

if __name__ == '__main__':
    parser = ArgumentParser(description='spectacle like program for resizing\
    and move windows in the mate desktop environment',
                            prog='mate-grid')
    parser.add_argument('-ml',
                        '--move-left',
                        action='store_true',
                        help='moves the window to the left half')
    parser.add_argument('-mr',
                        '--move-right',
                        action='store_true',
                        help='moves the window to the right half')
    parser.add_argument('-mt',
                        '--move-top',
                        action='store_true',
                        help='moves the window to the right half')
    parser.add_argument('-mb',
                        '--move-bottom',
                        action='store_true',
                        help='moves the window to the right half')
    parser.add_argument('-mtl',
                        '--move-top-left',
                        action='store_true',
                        help='moves the window to the top left quarter')
    parser.add_argument('-mtr',
                        '--move-top-right',
                        action='store_true',
                        help='moves the window to the top right quarter')
    parser.add_argument('-mbl',
                        '--move-bottom-left',
                        action='store_true',
                        help='moves the window to the bottom left quarter')
    parser.add_argument('-mbr',
                        '--move-bottom-right',
                        action='store_true',
                        help='moves the window to the bottom right quarter')
    parser.add_argument('-cm',
                        '--change-monitor',
                        action='store_true',
                        help='moves the window between monitors')

    args = parser.parse_args()
    main(args)
