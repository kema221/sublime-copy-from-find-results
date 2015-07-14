import sublime
import sublime_plugin
import re


class CopyFromFindResultsCommand(sublime_plugin.TextCommand):
    def run(self, edit, force=False):
        self.view.run_command('copy')

        if not self.in_find_results_view() and not force:
            return

        clipboard_contents = sublime.get_clipboard()

        if clipboard_contents:
            settings = sublime.load_settings('CopyFromFindResults.sublime-settings')
            keep_intermediate_dots = settings.get('keep_intermediate_dots', False)
            new_clipboard = RegexStruct2(keep_intermediate_dots).sub(clipboard_contents)
            new_clipboard2 = RegexStruct2(keep_intermediate_dots).sub(new_clipboard)
            sublime.set_clipboard(new_clipboard2)

    def in_find_results_view(self):
        return self.view.settings().get('syntax') == 'Packages/Default/Find Results.hidden-tmLanguage'


class RegexStruct():
    default = re.compile('^\s*\d+(\:\s|\s{2})', re.MULTILINE)
    without_dots = re.compile('^\s*(\d+(\:\s|\s{2})|\.+)', re.MULTILINE)

    def __init__(self, keep_dots=True):
        self.keep_dots = keep_dots

    def sub(self, text):
        return self.construct().sub('', text)

    def construct(self):
        return RegexStruct.default if self.keep_dots else RegexStruct.without_dots
class RegexStruct2():
    default = re.compile('^\s*\S+(\:\s|\s{2})', re.MULTILINE)
    without_dots = re.compile('^\s*(\S+(\:\s|\s{2})|\.+)', re.MULTILINE)

    def __init__(self, keep_dots=True):
        self.keep_dots = keep_dots

    def sub(self, text):
        return self.construct().sub('', text)

    def construct(self):
        return RegexStruct2.default if self.keep_dots else RegexStruct2.without_dots
