# Реалізація інформаційного та програмного забезпечення

В рамках проекту розробляється: 
- SQL-скрипт для створення на початкового наповнення бази даних
- RESTfull сервіс для управління даними
## SQL-скрипт для створення початкового наповнення бази даних

```
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE Projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('planned', 'in_progress', 'completed', 'on_hold'))
);

CREATE TABLE Tasks (
    id SERIAL PRIMARY KEY,
    project_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    priority INT CHECK (priority BETWEEN 1 AND 5),
    status VARCHAR(20) NOT NULL CHECK (status IN ('todo', 'in_progress', 'review', 'done')),
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES Projects(id) ON DELETE CASCADE
);

CREATE TABLE UserTasks (
    user_id INT NOT NULL,
    task_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, task_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES Tasks(id) ON DELETE CASCADE
);

CREATE TABLE Comments (
    id SERIAL PRIMARY KEY,
    task_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES Tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE Attachments (
    id SERIAL PRIMARY KEY,
    task_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(255) NOT NULL,
    filetype VARCHAR(50) NOT NULL,
    filesize INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES Tasks(id) ON DELETE CASCADE
);

INSERT INTO Users (username, email, password_hash) VALUES
('john_doe', 'john.doe@example.com', '$2a$10$xJwL5v5Jz7t6V7V7V7V7Ve'),
('jane_smith', 'jane.smith@example.com', '$2a$10$xJwL5v5Jz7t6V7V7V7V7Ve'),
('mike_johnson', 'mike.johnson@example.com', '$2a$10$xJwL5v5Jz7t6V7V7V7V7Ve');

INSERT INTO Projects (title, description, start_date, status) VALUES
('Website Redesign', 'Complete redesign of company website', '2024-01-15', 'in_progress'),
('Mobile App Development', 'Development of new mobile application', '2024-02-01', 'planned'),
('Marketing Campaign', 'Q2 marketing campaign preparation', '2024-03-01', 'planned');

INSERT INTO Tasks (project_id, title, description, priority, status) VALUES
(1, 'Design Homepage', 'Create new homepage design', 1, 'in_progress'),
(1, 'Develop Contact Form', 'Implement new contact form with validation', 2, 'todo'),
(2, 'App Prototyping', 'Create initial app prototype', 1, 'todo'),
(3, 'Market Research', 'Conduct target audience research', 3, 'todo');

INSERT INTO UserTasks (user_id, task_id) VALUES
(1, 1), (2, 2), (3, 3), (1, 4);

INSERT INTO Comments (task_id, user_id, content) VALUES
(1, 2, 'Please review the initial design concepts'),
(1, 1, 'Working on revisions based on feedback');

INSERT INTO Attachments (task_id, filename, filepath, filetype, filesize) VALUES
(1, 'design_concepts.pdf', '/uploads/design_concepts.pdf', 'application/pdf', 2540000);
```

# RESTfull сервіс для управління даними

## Підключення до бази даних

```
import pg from 'pg';
import dotenv from 'dotenv';

dotenv.config();

const pool = new pg.Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
});

export default pool;
```

## Моделі для роботи з даними

```
import pool from '../db.js';

export const getUserById = async (id) => {
  const result = await pool.query('SELECT * FROM Users WHERE id = $1', [id]);
  return result.rows[0];
};

export const createUser = async (username, email, passwordHash) => {
  const result = await pool.query(
    'INSERT INTO Users (username, email, password_hash) VALUES ($1, $2, $3) RETURNING *',
    [username, email, passwordHash]
  );
  return result.rows[0];
};
```

## Контролери для обробки запитів

```
import * as userModel from '../models/userModel.js';

export const getUser = async (req, res) => {
  try {
    const user = await userModel.getUserById(req.params.id);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }
    res.json(user);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

export const createUser = async (req, res) => {
  try {
    const newUser = await userModel.createUser(
      req.body.username,
      req.body.email,
      req.body.password
    );
    res.status(201).json(newUser);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};
```

## Маршрутизація
```
import express from 'express';
import { getUser, createUser } from '../controllers/userController.js';

const router = express.Router();

router.get('/:id', getUser);
router.post('/', createUser);

export default router;
```
