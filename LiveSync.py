#!/usr/bin/env python
import sublime
from os import popen
from sublime_plugin import EventListener


def make_file_names(src, dest, file_name):
    file_name = file_name.split(src)[1]
    src = src.replace(" ", "\\ ") + file_name
    dest = dest + file_name
    return (src, dest)


def rsync(exclude, settings, source, dest, ssh, view):
    dest = dest.replace(" ", "\\ ")
    if ssh:
        ssh = '-e ssh'
    else:
        ssh = ''

    source, dest = make_file_names(source, dest, view.file_name())
    print(111111, source, dest)
    cmd = "rsync %s --exclude %s -%s %s %s" % (source,
                                               exclude,
                                               settings,
                                               ssh,
                                               dest)
    view.set_status('uploading', 'uploading!!1')
    popen(cmd).read()
    view.set_status('uploading', 'done!!11')


class ShebangPythonListener(EventListener):
    def settings(self):
        return sublime.load_settings('LiveSync.sublime-settings')

    def rsync_dir(self, view):
        folders = sublime.active_window().folders()
        settings = self.settings()
        settings_folders = settings.get('folders')
        if not folders:
            return

        for folder in folders:
            folder_settings = settings_folders[folder]
            if not folder_settings:
                continue

            sync_settings = folder_settings['sync_settings']
            if not sync_settings:
                sync_settings = settings.get('sync_settings')

            exclude = folder_settings['exclude']
            if not exclude:
                exclude = settings.get('exclude')

            rsync(exclude,
                  sync_settings,
                  folder,
                  folder_settings['destination'],
                  folder_settings['ssh'],
                  view)

    def on_post_save_async(self, view):
        self.rsync_dir(view)
