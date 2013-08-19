#!/usr/bin/env python
import sublime
from sublime_plugin import EventListener

from .rsync.Rsync import Rsync


class LiveSync(EventListener):
    project = ''

    def settings(self):
        return sublime.load_settings('LiveSync.sublime-settings')

    def rsync_dir(self, folder_settings, view, folder, full_update=False):
        settings = self.settings()

        if 'sync_settings' not in folder_settings:
            sync_settings = settings.get('sync_settings')
        sync_settings = folder_settings['sync_settings']

        if 'exclude' not in folder_settings:
            exclude = settings.get('exclude')
        exclude = folder_settings['exclude']

        Rsync(view, {
            'source': folder,
            'destination': folder_settings['destination'],
            'ssh': folder_settings['ssh'],
            'settings': sync_settings,
            'exclude': exclude,
            'full_update': full_update
        })

    def rsync_dirs_if_needed(self, view):
        settings = self.settings()
        folders = sublime.active_window().folders()
        settings_folders = settings.get('folders')
        if not folders:
            return

        for folder in folders:
            if folder not in settings_folders:
                continue
            folder_settings = settings_folders[folder]
            self.rsync_dir(folder_settings, view, folder, False)

    def full_rsync_dirs_if_needed(self, view):
        settings = self.settings()
        folders = sublime.active_window().folders()
        settings_folders = settings.get('folders')
        if not folders:
            return

        for folder in folders:
            if folder not in settings_folders:
                continue
            folder_settings = settings_folders[folder]
            full = folder_settings['full_update_on_start']
            if full is None:
                full = settings.get('full_update_on_start')
            if not full:
                continue
            self.rsync_dir(folder_settings, view, folder, True)

    def on_post_save_async(self, view):
        self.rsync_dirs_if_needed(view)

    def on_activated_async(self, view):
        project = sublime.active_window().project_file_name()
        if project != self.project:
            self.project = project
            self.full_rsync_dirs_if_needed(view)
