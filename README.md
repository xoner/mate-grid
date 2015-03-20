# mate-grid

Simple program to move and resize windows with keyboard shortcuts for the mate desktop environment.

Inspired in functionality already present in other desktop environments (like gnome3, unity, kde, etc.) and other programs (like [spectacle](http://spectacleapp.com/) or [SizeUp](http://www.irradiatedsoftware.com/sizeup/) for Mac OS X) this little program brings to the mate desktop environment the ability to move windows between monitors and resize them to occupy any half or quarter of the current monitor.

## Requirements

### Ubuntu packages

* xdotool

### Python dependencies

* [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/), install it via `sudo apt-get install python-bs4` (preferred) or via pip.
* [sh](http://amoffat.github.io/sh/), install it via pip

## Installation

Install system packages:

    sudo apt-get install xdotool python-bs4 python-setuptools

Install python dependencies:
    
    sudo easy_install sh

Clone this repository:

    cd /opt    
    sudo git clone https://github.com/xoner/mate-grid.git

If you cloned the repository in a route other than /opt/mate-grid, edit the file create-shortcuts.py and change the value of the mate_grid_path to match the location of your cloned repository.

Run:
    
    python /opt/mate-grid/create-shortcuts.py

or

    python /path/to/cloned-repository/create-shortcuts.py 

if you cloned your repository in a route other than /opt



## Keyboard Shortcuts

Shortcut                                                                        |       Action
--------------------------------------------------------------------------------|--------------------------------
<kbd>Shift</kbd> + <kbd>Super</kbd> + <kbd>&#8592;</kbd>                        | Move window to previous monitor
<kbd>Shift</kbd> + <kbd>Super</kbd> + <kbd>&#8594;</kbd>                        | Move window to next monitor
<kbd>Super</kbd> + <kbd>&#8592;</kbd>                                           | Move window to the left half
<kbd>Super</kbd> + <kbd>&#8594;</kbd>                                           | Move window to the right half
<kbd>Ctrl</kbd> + <kbd>Super</kbd> + <kbd>&#8593;</kbd>                         | Move window to the top half
<kbd>Ctrl</kbd> + <kbd>Super</kbd> + <kbd>&#8595;</kbd>                         | Move window to the bottom half
<kbd>&#8679;</kbd> + <kbd>Ctrl</kbd> + <kbd>Super</kbd> + <kbd>&#8593;</kbd>    | Move window to the top left
<kbd>&#8679;</kbd> + <kbd>Ctrl</kbd> + <kbd>Super</kbd> + <kbd>&#8594;</kbd>    | Move window to the top right
<kbd>&#8679;</kbd> + <kbd>Ctrl</kbd> + <kbd>Super</kbd> + <kbd>&#8595;</kbd>    | Move window to the bottom right
<kbd>&#8679;</kbd> + <kbd>Ctrl</kbd> + <kbd>Super</kbd> + <kbd>&#8592;</kbd>    | Move window to the bottom left

You can edit this shortcuts to match your needs in the **Keyboard Shortcuts** section of the mate **Control Center**. They are installed under **Custom Shortcuts**.

## Todos

This program was developed in a Linux mint 17 mate machine with two monitors attached and only one panel located on the left monitor. There are many use cases that are not contemplated:

* [ ] Handle more than two monitors
* [ ] More than one panel in a single monitor
* [ ] Panels present on other monitors
* [ ] The program needs the existence of ~/.config/monitors.xml to know the monitors position and sizes, which is created once the monitor utility from the control center is opened. It should be created automatically if doesn't exist or get this information from other sources.
* [ ] The installation process should be automated via setup.py
* [ ] Better code documentation to adequate to PEP 257.