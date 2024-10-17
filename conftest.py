# conftest.py
import pytest  # Ajoutez cette ligne

def pytest_addoption(parser):
    parser.addoption("--file1", action="store", default="default1.txt", help="Specify the first file")
    parser.addoption("--file2", action="store", default="default2.txt", help="Specify the second file")

@pytest.fixture
def files(request):
    return request.config.getoption("--file1"), request.config.getoption("--file2")
