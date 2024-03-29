# Pytest Docker MongoDB

Provides fixtures for mongodb instances running in docker.

## Usage

Provided is the `db` fixture which gives you an `motor` test database instance
for mongodb.

```
@pytest.fixture
def db_with_schema(db_mongodb):
    fill_database(db_mongodb)
    return db
```

### Inside docker compose

This package also supports starting mongodb from `pytest` which itself is running inside
a container.

Included is a `docker-compose` file compatible with Google Cloud Build, this can be used by
passing the command line argument `--in-docker-compose=cloudbuild`.

In order to override the location of the `docker-compose.yml` you should write a
`docker_compose_files` fixture.

```
@pytest.fixture(scope="session")
def docker_compose_files(in_docker_compose, pytestconfig):
    # `in_docker_compose` gives you the value of the command line argument
    # you can use it to pick the location of the file
    # The following, for example, is used in this package
    dc_type = f".{in_docker_compose}" if in_docker_compose else ""

    dc_file = f"docker-compose{dc_type}.yml"
    return [os.path.join(os.path.dirname(__file__), dc_file)]
```
