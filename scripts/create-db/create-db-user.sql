CREATE USER flo_backend WITH PASSWORD 'flo_backend';
ALTER ROLE flo_backend SET client_encoding TO 'utf8';
ALTER ROLE flo_backend SET default_transaction_isolation TO 'read committed';
ALTER ROLE flo_backend SET timezone TO 'UTC';
ALTER USER flo_backend CREATEDB;


CREATE DATABASE flo_backend;
GRANT ALL PRIVILEGES ON DATABASE flo_backend TO flo_backend;
