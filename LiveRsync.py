#!/usr/bin/env python
import sublime
from sublime_plugin import EventListener
from sublime_plugin import WindowCommand
from sublime_plugin import TextCommand

from .rsync.RsyncHandler import RsyncHandler
from .rsync.RsyncLog import RsyncLogSingletone

controller = RsyncHandler()


class LiveRsync(EventListener):
    project = ''
    controller = controller

    def on_close(self, view):
        if view.name() == RsyncLogSingletone().get_log_view_name():
            RsyncLogSingletone().hide()

    def on_post_save_async(self, view):
        if self.controller.settings().get('auto_upload', True):
            self.controller.rsync(view)

    def on_activated_async(self, view):
        if not self.controller.settings().get('auto_upload', True):
            return
        project = sublime.active_window().project_file_name()
        if project != self.project:
            self.project = project
            self.controller.rsync(view, True)


class LiveRsyncUpdateLogViewCommand(TextCommand):
    def run(self, edit, value=''):
        self.view.insert(edit, 0, value)


class LiveRsyncUploadCurrent(WindowCommand):
    controller = controller

    def run(self, action=''):
        def callback():
            self.controller.rsync(sublime.active_window().active_view())
        sublime.set_timeout_async(callback, 0)


class LiveRsyncUploadFull(WindowCommand):
    controller = controller

    def run(self, action=''):
        def callback():
            self.controller.rsync(sublime.active_window().active_view(), True)
        sublime.set_timeout_async(callback, 0)


class LiveRsyncShowLog(WindowCommand):
    def run(self, action=''):
        RsyncLogSingletone().show()


class LiveRsyncDisable(WindowCommand):
    controller = controller

    def is_enabled(self):
        return self.controller.settings().get('auto_upload', True)

    def run(self, action=''):
        self.controller.settings().set('auto_upload', False)


class LiveRsyncEnable(WindowCommand):
    controller = controller

    def is_enabled(self):
        return not self.controller.settings().get('auto_upload', True)

    def run(self, action=''):
        self.controller.settings().set('auto_upload', True)
