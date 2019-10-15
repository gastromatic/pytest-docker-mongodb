import glob
import os

import pytest
import motor.motor_asyncio as motor


# We can either be on the host or in the docker-compose network
def pytest_addoption(parser):
    parser.addoption(
        "--in-docker-compose",
        action="store",
        default="",
        help="Assume inside a docker network",
    )


@pytest.fixture(scope="session")
def in_docker_compose(request):
    """
    Gets command line argument `--in-docker-compose`
    """
    return request.config.getoption("--in-docker-compose")


@pytest.fixture(scope="session")
def docker_compose_files(in_docker_compose, pytestconfig):
    """
    This fixture provides support for `cloudbuild`.
    By passing the command line argument `--in-docker-compose=cloudbuild`,
    uses `docker-compose.cloudbuild.yml`.
    """
    dc_type = f".{in_docker_compose}" if in_docker_compose else ""

    dc_file = f"docker-compose{dc_type}.yml"
    return [os.path.join(os.path.dirname(__file__), dc_file)]


def make_url(host: str, port: int) -> str:
    return f"mongodb://{host}:{port}/"


def wait_for_db(host: str, port: int) -> bool:
    url = make_url(host=host, port=port)
    try:
        motor.AsyncIOMotorClient(url)
        return True
    except Exception:
        return False


@pytest.fixture(scope="function")
def db_mongodb(in_docker_compose, docker_services):
    """
    Provided is the `db` fixture which gives you an `motor` test
    database instance for mongodb::

        @pytest.fixture
        def db_with_schema(db_mongodb):
            fill_database(db_mongodb)
            return db

    """
    docker_services.start("db")
    if in_docker_compose:
        port = 27017
        # Ugly but lovely-pytest-docker throws unnecessary exceptions
        docker_services.wait_until_responsive(
            timeout=30.0, pause=0.1, check=lambda: wait_for_db("db", port)
        )
    else:
        port = docker_services.wait_for_service("db", 27017, check_server=wait_for_db)
    host = "localhost" if not in_docker_compose else "db"
    url = make_url(host=host, port=port)
    client = motor.AsyncIOMotorClient(url)
    # yield a test database
    yield client['test']
    client.drop_database('test')
