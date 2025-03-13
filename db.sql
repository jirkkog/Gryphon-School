CREATE TABLE tests (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50),
    questions JSONB,
    correct_answers JSONB
);

CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    group VARCHAR(50),
    test_id INT REFERENCES tests(id),
    score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
