import sublime
from datetime import datetime

log = None


def RsyncLogSingletone():
    global log
    if log:
        return log

    log = RsyncLog()
    return log


class RsyncLog:
    panel = None

    def __init__(self):
        self.log = []

    def get_max(self):
        settings = sublime.load_settings('LiveRsync.sublime-settings')
        return settings.get('rsync_log_max', 50)

    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M") + '\n'

    def append(self, value):
        print('test1', value)
        value = self.get_time() + value
        self.log.append(value)
        if len(self.log) > self.get_max():
            self.log.pop(0)
        self.update(value)

    def show(self):
        window = sublime.active_window()
        self.panel = window.new_file()
        self.panel.set_scratch(True)
        self.panel.set_read_only(True)
        self.panel.set_name('LiveRsync Live Log')
        for log in self.log:
            self.update(log)
            print(log)
        window.run_command('show_panel', 'outputlive_rsync_output')

    def hide(self):
        self.panel = None

    def update(self, value):
        if not self.panel:
            return
        self.panel.run_command('live_rsync_update_log_view', {
            "value": value
        })
