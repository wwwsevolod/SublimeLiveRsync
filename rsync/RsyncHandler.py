from .Rsync import Rsync
import sublime


class RsyncHandler:
    def rsync(self, view, full=False):
        self.rsync_dirs(view, full)

    def settings(self):
        return sublime.load_settings('LiveRsync.sublime-settings')

    def get_folders_settings_array(self):
        window = sublime.active_window()
        project = window.project_data()
        if (project is None) or ('folders' not in project):
            return []
        folders = window.folders()
        project_data = project['folders']
        index = 0
        ready_settings = []

        for folder in folders:
            if 'live_rsync' not in project_data[index]:
                index += 1
                continue

            project_folder = project_data[index]['live_rsync']
            project_folder['source'] = folder
            settings = self.settings()
            if 'sync_settings' not in project_folder:
                sync_settings = settings.get('sync_settings')
                project_folder['sync_settings'] = sync_settings

            if 'exclude' not in project_folder:
                project_folder['exclude'] = settings.get('exclude')

            if 'full_update_on_start' not in project_folder:
                full = settings.get('full_update_on_start')
                project_folder['full_update_on_start'] = full

            ready_settings.append(project_folder)
            index += 1

        return ready_settings

    def rsync_dirs(self, view, try_full=False):
        folders = self.get_folders_settings_array()
        if not folders:
            return

        for folder in folders:
            if try_full:
                if not folder['full_update_on_start']:
                    continue
            Rsync(view, folder, try_full)
