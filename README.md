## Database

.env file
`DATABASE_URL="postgresql://root:password@localhost:5433/users"`

# SQL

## create user table

```sql
create table public.users (
id uuid primary key not null,
name VARCHAR(255),
email VARCHAR(255),
genre VARCHAR(255)
)
```

## insert user

```sql
insert into users values(gen_random_uuid(), 'User A', 'usera@gmail.com')
```

## docker-compose

### Env

```txt
CONTAINER_PREFIX=default-user

POSTGRES_VERSION=13
POSTGRES_PORT=5433
POSTGRES_USER=root
POSTGRES_DB=users
POSTGRES_PASSWORD=password

```

### docker-compose.yml

```yml
services:
  db:
    image: postgres:${POSTGRES_VERSION}
    container_name: postgres__${CONTAINER_PREFIX}
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    ports:
      - "${POSTGRES_PORT}:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
      - "./db/initial_data:/docker-entrypoint-initdb.d"

volumes:
  db_data:
    name: postgres__${CONTAINER_PREFIX}
```

## Folder Structure

- .env
- docker-compose.yml
- /db
  - /initial_data
    - sql.sql

## Run Python

Install all the dependencies: `python3 install -r requirements.txt`

Activate the envirnoment: `source .venv/bin/activate`

Run Flask: `flask run`
