import shutil
import tempfile
import unittest

import mock
import sh

import powerline_shell.segments.git_stash as git_stash
from powerline_shell.utils import RepoStats


class GitStashTest(unittest.TestCase):

    def setUp(self):
        self.powerline = mock.MagicMock()
        self.dirname = tempfile.mkdtemp()
        sh.cd(self.dirname)
        sh.git("init", ".")

        self.segment = git_stash.Segment(self.powerline, {})

    def tearDown(self):
        shutil.rmtree(self.dirname)

    @staticmethod
    def _add_and_commit(filename):
        sh.touch(filename)
        sh.git("add", filename)
        sh.git("commit", "-m", "add file " + filename)

    @staticmethod
    def _overwrite_file(filename, content):
        sh.echo(content, _out=filename)

    @staticmethod
    def _stash():
        sh.git("stash")

    @mock.patch('powerline_shell.utils.get_PATH')
    def test_git_not_installed(self, get_PATH):
        get_PATH.return_value = ""  # so git can't be found
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)

    def test_non_git_directory(self):
        shutil.rmtree(".git")
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)

    def test_no_stashes(self):
        self._add_and_commit("foo")
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)

    def test_one_stash(self):
        self._add_and_commit("foo")
        self._overwrite_file("foo", "some new content")
        self._stash()
        self.segment.start()
        self.segment.add_to_powerline()
        expected = u' {} '.format(RepoStats.symbols["stash"])
        self.assertEqual(self.powerline.append.call_args[0][0], expected)

    def test_multiple_stashes(self):
        self._add_and_commit("foo")

        self._overwrite_file("foo", "some new content")
        self._stash()

        self._overwrite_file("foo", "some different content")
        self._stash()

        self._overwrite_file("foo", "more different content")
        self._stash()

        self.segment.start()
        self.segment.add_to_powerline()
        expected = u' 3{} '.format(RepoStats.symbols["stash"])
        self.assertEqual(self.powerline.append.call_args[0][0], expected)
