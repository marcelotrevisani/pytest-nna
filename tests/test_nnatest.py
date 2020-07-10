
def test_bar_fixture(testdir, monkeypatch):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_sth():
            assert bar == "europython2015"
        
        def test_pass():
            assert True
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        "--username='username'",
        "--token='1345'",
        "--test-run-id='123'",
        "--report-url-api='testing.com.br'",
    )

    # fnmatch_lines does an assertion internally
    # result.stdout.fnmatch_lines([
    #     '*::test_sth PASSED*',
    # ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'pytest_nna:',
        '*--foo=DEST_FOO*Set the value for the fixture "bar".',
    ])


def test_hello_ini_setting(testdir):
    testdir.makeini("""
        [pytest]
        HELLO = world
    """)

    testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def hello(request):
            return request.config.getini('HELLO')

        def test_hello_world(hello):
            assert hello == 'world'
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_hello_world PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
