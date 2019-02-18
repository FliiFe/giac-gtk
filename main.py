from giacgtk.mainwindow import MainWindow
from giacgtk.latexrenderer import render_latex
from giacgtk.giacutil import GiacInstance
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def run_callback(widget, pos, event, cell):
    global giac_instance
    command = widget.get_text()
    print('got input:', command)
    result = giac_instance.exec_command(command)
    print(result)
    svg = ''
    mode = get_mode_from_output(result)
    content = get_content_without_mode(result)
    if mode == 'latex':
        svg = render_latex(content, fg=win.foreground)
    elif mode == 'verbatim':
        svg = render_latex(content, fg=win.foreground, template='verbatim')
    if svg:
        print(svg)
        win.set_cell_output(cell, result, svg)


def get_mode_from_output(output):
    return output.split(':')[0]


def get_content_without_mode(output):
    return ':'.join(output.split(':')[1:])


def quit(win):
    global giac_instance
    giac_instance.destroy()
    Gtk.main_quit(win)


if __name__ == "__main__":
    giac_instance = GiacInstance()

    win = MainWindow(run_callback)
    win.connect("destroy", quit)
    win.show_all()
    Gtk.main()
