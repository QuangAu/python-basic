# Python fundamentals and FastApi sample project

## Introduction

A simple REST api collection to manage football players and their clubs.

Supported APIs:

- Create / Update player.
- Create / Update club.
- Search players / clubs based on specific conditions.
- Assign player to club.
- Create player's transfer history.
- Create / Update / Delete user.
- Allow logging in user to change their own password.
- Authentication with 2 different flows: password & client_credentials.

## Technical stack

- Programming language: Python
- Framework: FastApi, SqlAlchemy, Alembic
- Database: SQLite or Postgresql

## Extra implementation

- Easily switch DB engine between Postgres and SQLite, using `dependencies` module.
- Introduce new class `OAuth2PasswordRequestFormNoStrict` to allow client_credentials grant_type rather than password only.
- Design a table transfer_history with 2 foreign keys reference to one table (club). `aliased` keyword is used to query data based on both foreign keys.

## Build and run

1. Install required packages: `pip install -r requirements.txt`
2. Update `dev.env` file to configure database engine and its connection.
3. Run `alembic upgrade head` for DB migration. (If postgres DB is used, make sure the DB is created in prior).
4. Change directory (`cd`) to `app` folder then run command: `uvicorn main:app --reload`
