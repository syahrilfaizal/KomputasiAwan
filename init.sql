CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

INSERT INTO items (name, description) VALUES
('Test Item', 'This is a test description'),
('Test Item 2', 'This is a test description 2');