# Django Dockerized Project

This project is a Django application that runs in a Docker container using Docker Compose. It uses SQLite as the database and runs on port 8080.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Create a `.env` File**

   Create a `.env` file in the root of the project and add the following environment variables:

   ```bash
   SECRET_KEY=<your_secret_key>
   ```

3. **Build and Run the Containers**

   Build and run the containers using Docker Compose:

   ```bash
   docker-compose up --build
   ```

4. **Create a Superuser**

   To create a Django superuser, run the following command:

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the Application**

   The Django application will be available at:

   ```
   http://localhost:8080
   ```

## Project Structure

- **Dockerfile**: Defines the environment setup for the Django app.
- **docker-compose.yml**: Manages the `web` and `db` services.
- **requirements.txt**: Python dependencies.
- **db.sqlite3**: SQLite database file, mounted as a volume to persist data.

## Docker Compose Services

- **web**: Django application container, accessible at `localhost:8080`.
- **db**: SQLite container, data persisted in the `db.sqlite3` file.

## Running Migrations

To apply Django database migrations:

```bash
docker-compose exec web python manage.py migrate
```

## Debug Mode

By default, the project is in debug mode. To disable debug mode, update the `.env` file and rebuild the container:

```bash
DEBUG=0
```

## Stopping the Containers

To stop and remove the containers, run:

```bash
docker-compose down
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
