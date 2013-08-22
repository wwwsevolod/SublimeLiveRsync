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
        self.logs = []

    def get_log_view_name(self):
        return 'LiveRsync Live Log'

    def get_max(self):
        settings = sublime.load_settings('LiveRsync.sublime-settings')
        return settings.get('rsync_log_max', 50)

    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M") + ':\n'

    def log(self, value):
        value = self.get_time() + value
        self.logs.append(value + '\n\n')
        if len(self.logs) > self.get_max():
            self.logs.pop(0)
        self.update(value)

    def get_log_view(self, window):
        for view in window.views():
            if view.name() == self.get_log_view_name():
                return view

        return None

    def show(self):
        window = sublime.active_window()
        log_view = self.get_log_view(window)
        if log_view:
            self.panel = log_view
            window.focus_view(log_view)
        else:
            self.panel = window.new_file()
            self.panel.set_scratch(True)
            self.panel.set_name(self.get_log_view_name())
        for log in self.logs:
            self.update(log)

    def hide(self):
        self.panel = None

    def update(self, value):
        if not self.panel:
            return
        self.panel.set_read_only(False)
        self.panel.run_command('live_rsync_update_log_view', {
            "value": value
        })
        self.panel.set_read_only(True)
