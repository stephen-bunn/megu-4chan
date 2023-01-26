from pytest import fixture

from megu_4chan.utils import get_thread_url

TEST_THREAD_BOARD = "test"
TEST_THREAD_ID = "123456789"


@fixture
def thread_board_url():
    return f"https://boards.4chan.org/{TEST_THREAD_BOARD}/thread/{TEST_THREAD_ID}"


@fixture
def thread_api_url():
    return get_thread_url(TEST_THREAD_BOARD, TEST_THREAD_ID)
