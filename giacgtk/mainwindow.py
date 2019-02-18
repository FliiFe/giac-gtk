import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class MainWindow(Gtk.Window):

    def __init__(self, run_callback):
        self.cells = []
        self.cellcount = 0
        self.run_callback = run_callback

        Gtk.Window.__init__(self, title="Giac GTK")
        self.set_border_width(10)
        self.set_default_size(400, 200)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_decoration_layout("menu:minimize,close")
        hb.props.title = "Giac GTK"
        self.set_titlebar(hb)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-new-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        button.connect("clicked", self.add_cell)
        hb.pack_end(button)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.DOWN, Gtk.ShadowType.NONE))
        box.add(button)

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.UP, Gtk.ShadowType.NONE))
        box.add(button)

        hb.pack_start(box)

        img = Gtk.Image.new_from_file('/tmp/latex-test/main.svg')

        self.body = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.add(self.body)

        self.add_cell()

        state = self.get_state()
        self.fgColor = self.get_style_context().get_color(state)

    @property
    def foreground(self):
        return [self.fgColor.red, self.fgColor.green, self.fgColor.blue]

    def add_cell(self, button=None):
        entry = Gtk.Entry()
        entry.set_icon_from_icon_name(
            Gtk.EntryIconPosition.SECONDARY, 'go-next-symbolic')
        entry.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY, 'Run')
        entry.connect("icon-press", self.run_callback, self.cellcount)
        output = Gtk.Image.new()
        self.body.pack_start(entry, False, True, 0)
        self.body.pack_start(output, False, True, 10)
        self.cells.append({
            'entry': entry,
            'output': output,
            'outputtext': '',
            'cellno': self.cellcount,
            'visible': True
        })
        self.cellcount += 1
        self.show_all()

    def remove_cell(self, cell):
        self.cells[cell]['entry'].hide()
        self.cells[cell]['output'].hide()
        self.cells[cell]['visible'] = False

    def set_cell_output(self, cell, output, svg):
        self.cells[cell]['outputtext'] = output
        self.cells[cell]['output'].set_from_file(svg)
