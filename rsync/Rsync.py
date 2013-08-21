from os import popen
from .RsyncLog import RsyncLogSingletone


class Rsync(object):
    def __init__(self, view, settings, full):
        self.view = view
        self.prepare(settings, full)
        self.query(self.generate_cmd())

    def prepare(self, settings, full):
        self.source = settings['source']
        self.destination = settings['destination']
        self.ssh = settings['ssh']
        self.full_update = settings['full_update_on_start'] if full else False
        self.settings = settings['sync_settings']
        self.exclude = settings['exclude']

    def generate_cmd(self):
        src = self.source.replace(" ", "\\ ")
        dest = self.destination.replace(" ", "\\ ")
        file_name = self.view.file_name()
        exclude = self.exclude
        if not self.full_update:
            src, dest = self.make_file_names(src, dest, file_name)
        else:
            src += '/'
        if self.ssh:
            ssh = '-e ssh'
        else:
            ssh = ''
        cmd = "rsync " + src + " --exclude " + exclude
        cmd = cmd + " -" + self.settings
        cmd = cmd + " " + ssh + " " + dest
        return cmd

    def query(self, cmd):
        self.view.set_status('uploading', 'uploading!!1')
        log = RsyncLogSingletone()
        log.log(cmd)
        log.log(popen(cmd).read())
        self.view.set_status('uploading', 'done!!11')

    def make_file_names(self, src, dest, file_name):
        file_name = file_name.split(src)[1]
        src = src + file_name
        dest = dest + file_name
        return (src, dest)
