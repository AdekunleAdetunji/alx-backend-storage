-- A script to create an sql user table with the requirements
    -- id: integer, never null, auto increment and primary key
    -- email: string (255 characters), never null and unique
    -- name: string (255 characters)

CREATE DATABASE IF NOT EXISTS holberton;

USE holberton;
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);