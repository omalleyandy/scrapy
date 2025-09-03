import io
from ftplib import FTP, error_perm
from unittest import mock

from scrapy.utils.ftp import ftp_store_file
from tests.mockserver import MockFTPServer


def test_ftp_makedirs_ignore_existing_dir():
    with MockFTPServer() as ftp_server:
        orig_mkd = FTP.mkd

        def mkd_then_exists(self, path):
            # create the directory then behave as if it already existed
            orig_mkd(self, path)
            raise error_perm("550 File exists.")

        with mock.patch("ftplib.FTP.mkd", new=mkd_then_exists):
            ftp_store_file(
                path="dir/subdir/file",
                file=io.BytesIO(b"data"),
                host="127.0.0.1",
                port=2121,
                username="",
                password="",
            )
        assert (ftp_server.path / "dir/subdir/file").read_bytes() == b"data"

