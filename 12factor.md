# 12-Factor App Methodology for Python (Updated 2026)

A guide to building modern, scalable, and maintainable Python applications following the [12-Factor App](https://12factor.net/) principles.

---

## 1. Codebase
**One codebase tracked in revision control, many deploys.**
- **Strategy:** Use **GitHub Flow** (or GitLab Flow). Maintain a single `main` branch as the source of truth.
- **Trunk-Based Development:** Avoid long-lived "environment branches" (e.g., `prod-branch`). Differentiate deployments strictly via Configuration (Factor 3).
- **One-to-One:** One repository = one app/service. Shared logic should be moved to internal libraries.

## 2. Dependencies
**Explicitly declare and isolate dependencies.**
- **Tooling:** Use **`uv`** for lightning-fast dependency management and virtual environment isolation.
- **Deterministic Builds:** Always commit your `uv.lock` file. This ensures that every developer and CI/CD runner uses the exact same dependency tree.
- **Isolation:** Never rely on system-level Python packages; use `uv run` or `uv venv` to ensure a clean runtime.

## 3. Config
**Store config in the environment.**
- **Recommended Tool:** **`pydantic-settings`**. It provides type-safe validation, ensuring the app "fails fast" if an environment variable is missing or malformed.
- **Secrets:** Use `SecretStr` for sensitive data (API keys, passwords) to prevent accidental leakage in logs.
- **Precedence:** Use `.env` files for local development convenience, but ensure system environment variables take precedence in production.



## 4. Backing Services
**Treat backing services as attached resources.**
- Databases (PostgreSQL), Caches (Redis), and Message Brokers (RabbitMQ) are accessed via URLs.
- **Abstraction:** Use an ORM (SQLAlchemy, Tortoise) or an interface that allows swapping a local instance for a managed cloud service (e.g., AWS RDS) via a simple connection string change.

## 5. Build, Release, Run
**Strictly separate build and run stages.**
- **Build:** `uv lock` + Dockerfile. The result is an immutable artifact (Docker Image).
- **Release:** The Image combined with specific environment variables (Config).
- **Run:** The execution of the container. 
- **Immutable Rule:** Never "hot-fix" code directly on a server. Every change must go through the Build -> Release -> Run pipeline.

## 6. Processes
**Execute the app as one or more stateless processes.**
- **Statelessness:** Python processes should share nothing. Use **Redis** for sessions and **S3/Minio** for file storage.
- **Scaling:** If a process crashes or is restarted, no data should be lost.

## 7. Port Binding
**Export services via port binding.**
- **ASGI/WSGI:** Use **Uvicorn** (for async/FastAPI) or **Gunicorn** (for WSGI/Django/Flask).
- **Self-Contained:** The app is responsible for listening on a port (e.g., `$PORT`). Do not assume an external proxy like Nginx is handling the protocol logic inside the container.

## 8. Concurrency
**Scale out via the process model.**
- **Internal Scaling:** Use a process manager like Gunicorn with multiple workers to utilize all CPU cores within a single container.
- **External Scaling:** Use a container orchestrator (Kubernetes/Docker Swarm) to scale the number of containers horizontally.



## 9. Disposability
**Maximize robustness with fast startup and graceful shutdown.**
- **Startup:** Keep the app's initialization logic lean. 
- **Shutdown:** Catch `SIGTERM` signals to close database connections and finish processing current requests before the process exits.

## 10. Dev/Prod Parity
**Keep development, staging, and production as similar as possible.**
- **Tooling:** Use **Docker Compose** to run the exact same versions of PostgreSQL, Redis, and Python locally as you do in production.
- **Parity:** Avoid using SQLite for development if you use PostgreSQL in production; subtle differences in SQL syntax can cause production-only bugs.

## 11. Logs
**Treat logs as event streams.**
- **No Log Files:** Do not write to `/var/log`. 
- **Standard Out:** Use the standard Python `logging` module to write to `stdout`. 
- **Infrastructure:** Let your log aggregator (ELK stack, Datadog, CloudWatch) capture the stream from the container's output.

## 12. Admin Processes
**Run admin/management tasks as one-off processes.**
- **Migrations:** Run `alembic upgrade head` or `django-admin migrate` as a separate, one-off task within the same environment/release.
- **Consistency:** Admin scripts must use the same dependency lockfile and configuration as the web processes.

---
*Created for py_examples repository.*
