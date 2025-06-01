import rumps

# u = ["𝟷", "𝟸", "𝟹", "𝟺", "𝟻", "𝟼", "𝟽", "𝟾", "𝟿", "𝟶", "𝟷", "𝟸", "𝟹"]
# f = ["1̲", "2̲", "3̲", "4̲", "5̲", "6̲", "7̲", "8̲", "9̲", "0̲", "1̲", "2̲", "3̲"]
# n = ["∙", "∙", "∙", "∙", "∙", "∙", "∙", "∙", "∙", "∙", "∙", "∙", "∙"]
f = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "𝟎", "𝟏", "𝟐", "𝟑"]
e = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⓪", "①", "②", "③"]
u = ["𝟏", "𝟐", "𝟑", "𝟒", "𝟓", "𝟔", "𝟕", "𝟖", "𝟗", "𝟎", "𝟏", "𝟐", "𝟑"]
n = e
NSPC = {i + 1: n[i] for i in range(len(e))}
USPC = {i + 1: u[i] for i in range(len(u))}
ESPC = {i + 1: e[i] for i in range(len(e))}
FSPC = {i + 1: f[i] for i in range(len(f))}


class YabaiMenuApp(rumps.App):
    def __init__(self):
        S.app = self
        super().__init__("", title="", quit_button=None)
        self.icon_path = None

    def set_title(self):
        t = ""
        for v in S.menutitle.values():
            t += v
        self.title = t

    def add(self, title, cb, ico=None, parent=None):
        parent = self.menu if parent is None else parent
        if callable(cb) or cb is None:
            parent.add(rumps.MenuItem(title, callback=cb, icon=ico))
        else:
            m = rumps.MenuItem(title, icon=ico)
            [self.add(*k, parent=m) for k in cb]
            parent.add(m)


def quit_app(_):
    log("Quitting...")
    rumps.quit_application()


log = print


class Events:
    """Base class for event handlers. Event modules import this and add their handlers."""
    
    def none(self, evt):
        print(evt)


class S:
    menutitle = {}
    fn_fifo = ""
    cur_win = {}
    app: YabaiMenuApp = None
    spaces: list = []
    strspaces = ""
    windows = {}
    rebuild = False
    lognr = 0
