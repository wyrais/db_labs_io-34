-- Удаление существующих таблиц (если нужно пересоздать)
-- DROP TABLE IF EXISTS attachments CASCADE;
-- DROP TABLE IF EXISTS comments CASCADE;
-- DROP TABLE IF EXISTS usertasks CASCADE;
-- DROP TABLE IF EXISTS tasks CASCADE;
-- DROP TABLE IF EXISTS projects CASCADE;
-- DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('planned', 'in_progress', 'completed', 'on_hold'))
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    project_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    priority INT CHECK (priority BETWEEN 1 AND 5),
    status VARCHAR(20) NOT NULL CHECK (status IN ('todo', 'in_progress', 'review', 'done')),
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE usertasks (
    user_id INT NOT NULL,
    task_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, task_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    task_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE attachments (
    id SERIAL PRIMARY KEY,
    task_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(255) NOT NULL,
    filetype VARCHAR(50) NOT NULL,
    filesize INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- Вставка тестовых данных
INSERT INTO users (username, email, password_hash) VALUES
('john_doe', 'john.doe@example.com', '$2a$10$xJwL5v5Jz7t6V7V7V7V7Ve'),
('jane_smith', 'jane.smith@example.com', '$2a$10$xJwL5v5Jz7t6V7V7V7V7Ve'),
('mike_johnson', 'mike.johnson@example.com', '$2a$10$xJwL5v5Jz7t6V7V7V7V7Ve');

INSERT INTO projects (title, description, start_date, status) VALUES
('Website Redesign', 'Complete redesign of company website', '2024-01-15', 'in_progress'),
('Mobile App Development', 'Development of new mobile application', '2024-02-01', 'planned'),
('Marketing Campaign', 'Q2 marketing campaign preparation', '2024-03-01', 'planned');

INSERT INTO tasks (project_id, title, description, priority, status) VALUES
(1, 'Design Homepage', 'Create new homepage design', 1, 'in_progress'),
(1, 'Develop Contact Form', 'Implement new contact form with validation', 2, 'todo'),
(2, 'App Prototyping', 'Create initial app prototype', 1, 'todo'),
(3, 'Market Research', 'Conduct target audience research', 3, 'todo');

INSERT INTO usertasks (user_id, task_id) VALUES
(1, 1), (2, 2), (3, 3), (1, 4);

INSERT INTO comments (task_id, user_id, content) VALUES
(1, 2, 'Please review the initial design concepts'),
(1, 1, 'Working on revisions based on feedback');

INSERT INTO attachments (task_id, filename, filepath, filetype, filesize) VALUES
(1, 'design_concepts.pdf', '/uploads/design_concepts.pdf', 'application/pdf', 2540000);