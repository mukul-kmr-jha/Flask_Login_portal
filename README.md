## Flask_Login_Portal

A simple and interesting login portal built with python as a back-end

This web app uses
- Flask Microframework
- Postgres
- Flask-SQLAlchemy

Instructions to run it locally:

- Duplicate the environment by using following command

   `conda create --name <envname> --file requirements.txt`

- Switch to the newly created environment

  `conda activate <envname>`
- set the environment variable (For Linux)

  ` $ export FLASK_APP=app  `

  `$ export FLASK_ENV=development`

  `$ export DATABASE_URI='postgresql://<your-postgres-user>:<password>@localhost:5432/<your-testing-db>' `
-   Finally run the application
  `flask run`
