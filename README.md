# Schedule Manager Backend Project Documentation

## Development

### Project Requirements

- Python 3.11+
- Virtualenv 20.24
- Docker Engine 20.10+
- Docker Compose 1.29+

### IDE

I recommend you use Visual Studio Code and set it up using the ff. extensions and settings below.

##### Extensions

Install these extensions in VS Code:

- Python
- Django
- Pylint
- Flake8
- MyPy Type Checker

### Swagger Endpoint

http://127.0.0.1:8000/swagger/

##### Settings

VSCode workspace settings are already included in the project (_.vscode/settings.json_)

### Project Setup (Without using Docker)

1. Clone the project

```bash
  git clone https://github.com/ooplaza/schedule-manager.git
```

2. Create a virtual environment using virtualenv running on Python 3.11

```bash
  python3 -m venv venv # windows virtualenv <env_name>
```

3. Activate the virtual environment

```bash
  source venv/bin/activate
```

4. Run the command to install local environment dependencies.

```bash
  pip install -r requirements.txt
```

5. **Run database migrations and collectstatic:**

   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic
   ```

6. **Create a superuser:**

   ```
   python manage.py createsuperuser
   ```

7. Run the test case and if it's success then youre good to go.

```bash
   python manage.py test --parallel
```

### Docker Project Setup

1. Run command this command.

```bash
docker-compose up --build (or `docker compose up --build` if already supporting Docker Compose v2).
```

2. Ensure you have a host that matches the server_name in the `nginx.conf` file in the root director. For macs edit your /etc/host
```bash
127.0.0.1 schedule_manager-be.test
```

3. Run the migration command command

```bash
docker exec -it schedule_manager-be python manage.py migrate
```

### Running and shutting down the development server

1. Make sure that the [project setup](#project-setup) is done
2. While the Docker Engine is running, run the command `docker compose up -d` to start up the database container
3. Make sure to check if there are new migrations, and apply them if necessary
4. Run the command `python manage.py runserver` to start the development server. Server is available at http://127.0.0.1:8000/
5. To quit the development server, use `CONTROL-C`. After that, shut down the database container using `docker compose down`

### Running tests

- Use the command `python manage.py test --parallel` to run all unit testcase classes in parallel
- Using coverage: `coverage run manage.py test --parallel` and `coverage html` for the report.

### Running tests via container

- docker exec -it schedule_manager-be python manage.py test --parallel

### How I implemented JWT

There are many ways to implement JWT authentication based system. How I Customize and implementation was by installing the dj_rest_auth library then after that my serializer class CustomTokenObtainPairSerializer inherited from this class provided from dj_rest_auth (TokenObtainPairSerializer) and by using some validation, then after that I called this CustomTokenObtainPairSerializer into my LoginView also I modified the response to set the JWT into cookie only so that the JavaScript won't be able to access it but this is just an optional by including this is_http_cookie_only in the payload then after that if the serializer is valid return the token in cookie only if is_http_cookie_only is False else return the expiration only.
