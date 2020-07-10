import os
from pathlib import Path

import pytest
import requests

from pytest_nna.arca_components import ArcaComponent


def pytest_addoption(parser):
    group = parser.getgroup('pytest_nna')
    group.addoption(
        '--collection-output',
        action='store',
        dest='collection_output',
        metavar="path",
        default=None,
        help='Path to the file where the collection will be dumped'
    )
    group.addoption(
        '--report-url-api',
        action='store',
        dest='report_url_api',
        default=None,
        help="URL to the API endpoint",
    )
    group.addoption(
        '--username',
        action='store',
        dest='username',
        default=None,
        help="API Username to be authenticated",
    )
    group.addoption(
        '--token',
        action='store',
        dest='token',
        default=None,
        help="Token to authenticate the user",
    )
    group.addoption(
        '--test-run-id',
        action='store',
        dest='test_run_id',
        default=None,
        help="Test run identification",
    )


def write_tests_collection(file_path, items_list):
    """This function is responsible to write the file with the test collection
    content.
    :param str file_path: Path to the file where it will be printed
    :param List(_pytest.nodes.Item] items: test list
    """
    if not file_path or not items_list:
        return

    file_path = Path(file_path)

    if file_path.exists() and file_path.is_dir():
        file_path = file_path / "tests.txt"

    with open(file_path, 'w') as collection_file:
        for item in items_list:
            path_test, _, test_call = item.location
            out_str = f"{path_test} {test_call}\n"
            collection_file.write(out_str)


class NNAPlugin:

    def __init__(self, config):
        self._file_path_collection = config.getvalue("collection_output")
        self._api_url = config.getvalue("report_url_api")
        self._username = config.getvalue("username")
        self._token = config.getvalue("token")
        self._test_run_id = config.getvalue("test_run_id")

    @property
    def auth(self):
        return (self._username, self._token)

    def pytest_report_collectionfinish(self, config, startdir, items):
        if self._file_path_collection:
            write_tests_collection(self._file_path_collection, items)

    def pytest_runtest_makereport(self, item, call):
        if self._api_url and self._username and self._token and self._test_run_id:
            url = self._api_url.strip()
            if not url.endswith("/"):
                url += f"{url}/"
            url = f"{url}tests/single-test/"

            os_info = os.uname()
            error_msg = ""
            if call.result:
                error_msg = f"{call.excinfo.typename}: {call.excinfo.value}"

            requests.post(
                url,
                auth=self.auth,
                data={
                    "run_test_id": self._test_run_id,
                    "result": "FAIL" if error_msg else "PASS",
                    "node_id": item.nodeid,
                    "step": call.when,
                    "duration": call.stop - call.start,
                    "error": error_msg,
                    "sys_name": os_info.sysname,
                    "hostname": os_info.nodename,
                    "sys_release": os_info.release,
                    "sys_version": os_info.version,
                    "sys_machine": os_info.machine,
                    "extra_info": item.user_properties,
                },
            )

def pytest_configure(config):
    config.pluginmanager.register(NNAPlugin(config), "_nna")


@pytest.fixture(scope="function")
def components():
    return ArcaComponent()


@pytest.fixture(scope="function")
def component_log(record_property):
    extra = {}
    record_property("log_extra", extra)
    return extra
