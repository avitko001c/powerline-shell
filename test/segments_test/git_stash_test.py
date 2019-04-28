import unittest
import mock
import tempfile
import shutil
import sh
import powerline_shell.segments.git_stash as git_stash
from powerline_shell.utils import RepoStats


def _stash():
    sh.git("stash")


def _overwrite_file(filename, content):
    sh.echo(content, _out=filename)


def _add_and_commit(filename):
    sh.touch(filename)
    sh.git("add", filename)
    sh.git("commit", "-m", "add file " + filename)


class GitStashTest(unittest.TestCase):

    def setUp(self):
        self.powerline = mock.MagicMock()
        self.dirname = tempfile.mkdtemp()
        sh.cd(self.dirname)
        sh.git("init", ".")

        self.segment = git_stash.Segment(self.powerline, {})

    def tearDown(self):
        shutil.rmtree(self.dirname)

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
        _add_and_commit("foo")
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)

    def test_one_stash(self):
        _add_and_commit("foo")
        _overwrite_file("foo", "some new content")
        _stash()
        self.segment.start()
        self.segment.add_to_powerline()
        expected = u' {} '.format(RepoStats.symbols["stash"])
        self.assertEqual(self.powerline.append.call_args[0][0], expected)

    def test_multiple_stashes(self):
        _add_and_commit("foo")

        _overwrite_file("foo", "some new content")
        _stash()

        _overwrite_file("foo", "some different content")
        _stash()

        _overwrite_file("foo", "more different content")
        _stash()

        self.segment.start()
        self.segment.add_to_powerline()
        expected = u' 3{} '.format(RepoStats.symbols["stash"])
        self.assertEqual(self.powerline.append.call_args[0][0], expected)
