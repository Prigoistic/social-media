-- Create posts table if it doesn't exist
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    published BOOLEAN DEFAULT TRUE,
    rating INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO posts (title, content, published, rating) VALUES
    ('First Post', 'This is the content of the first post', true, 5),
    ('Second Post', 'This is the content of the second post', false, 3),
    ('Third Post', 'This is the content of the third post', true, 4)
ON CONFLICT (id) DO NOTHING; 