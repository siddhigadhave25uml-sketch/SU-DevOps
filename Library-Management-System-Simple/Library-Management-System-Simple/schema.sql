CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;
CREATE TABLE IF NOT EXISTS books (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  author VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO books (title, author) VALUES
('The Alchemist', 'Paulo Coelho'),
('Wings of Fire', 'A. P. J. Abdul Kalam'),
('Pride and Prejudice', 'Jane Austen');
