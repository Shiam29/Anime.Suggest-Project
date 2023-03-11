-- Drop the tables before creating them. That way re-running this file and
-- seed.l` will "restart" the database with a clean slate.
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS anime CASCADE;

CREATE DATABASE library;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50),
  email VARCHAR(50),
  password TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE anime (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50),
  year INT,
  image_url VARCHAR(200)
);
