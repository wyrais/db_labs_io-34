# Реалізація інформаційного та програмного забезпечення

В рамках проекту розробляється: 
- SQL-скрипт для створення на початкового наповнення бази даних
- RESTfull сервіс для управління даними
## SQL-скрипт для створення початкового наповнення бази даних

```
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

## Налаштування сервера
```
import express from 'express';
import userRouter from './routes/userRoutes.js';
import projectRouter from './routes/projectRoutes.js';
import taskRouter from './routes/taskRoutes.js';

const app = express();

app.use(express.json());

app.use('/api/users', userRouter);
app.use('/api/projects', projectRouter);
app.use('/api/tasks', taskRouter);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

## Запуск сервера 

```
import app from './app.js';
import dotenv from 'dotenv';

dotenv.config();

const startServer = () => {
  const port = process.env.PORT || 3000;
  app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
  });
};

startServer();
```
## Маршрути для User та MediaContent


### Маршрути для User

```
// routes/userRoutes.js

import express from 'express';
import {
  registerUser,
  listUsers,
  getUser,
  updateUser,
  removeUser,
} from '../controllers/userController.js';

const userRouter = express.Router();

userRouter.post('/user', registerUser);
userRouter.get('/user', listUsers);
userRouter.get('/user/:id', getUser);
userRouter.patch('/user/:id', updateUser);
userRouter.delete('/user/:id', removeUser);

export default userRouter;
```
### Маршрути для MediaContent

```
import express from 'express';
import {
  createMediaContent,
  getMediaContents,
  getMediaContent,
  updateMediaContent,
  deleteMediaContent,
} from '../controllers/mediaContentController.js';

const mediaContentRouter = express.Router();

mediaContentRouter.post('/content', createMediaContent);
mediaContentRouter.get('/content', getMediaContents);
mediaContentRouter.get('/content/:id', getMediaContent);
mediaContentRouter.patch('/content/:id', updateMediaContent);
mediaContentRouter.delete('/content/:id', deleteMediaContent);

export default mediaContentRouter;
```
## Контролери для User

```
import {
  createProfile,
  fetchAllProfiles,
  findUserById,
  updateProfileById,
  deleteProfileById,
  findUserByEmail,
} from '../models/userModel.js';
import AppError from '../utils/appError.js';
import handleAsync from '../utils/handleAsync.js';
import { validateRequiredFields } from '../utils/validator.js';

export const registerUser = handleAsync(async (req, res) => {
  const userData = req.body;
  validateRequiredFields(userData);
  const existing = await findUserByEmail(userData.email);
  if (existing) {
    throw new AppError('AlreadyRegisteredException', 400);
  }
  await createProfile(userData);
  res.status(201).json({ status: 'success', message: 'User registered successfully' });
});

export const listUsers = handleAsync(async (req, res) => {
  const users = await fetchAllProfiles();
  res.status(200).json({ status: 'success', message: users });
});

export const getUser = handleAsync(async (req, res) => {
  const { id } = req.params;
  const user = await findUserById(id);
  if (!user) {
    throw new AppError('UserNotFoundException', 404);
  }
  res.status(200).json({ status: 'success', message: user });
});

export const updateUser = handleAsync(async (req, res) => {
  const { id } = req.params;
  const updates = req.body;
  const user = await findUserById(id);
  if (!user) {
    throw new AppError('UserNotFoundException', 404);
  }
  const updated = await updateProfileById(id, updates);
  res.status(200).json({ status: 'success', message: 'User updated successfully', updatedUser: updated });
});

export const removeUser = handleAsync(async (req, res) => {
  const { id } = req.params;
  const user = await findUserById(id);
  if (!user) {
    throw new AppError('UserNotFoundException', 404);
  }
  await deleteProfileById(id);
  res.status(200).json({ status: 'success', message: 'User deleted successfully' });
});
```
## Взаємодія з базою даних для User

```
import pool from '../db.js';

export const createProfile = async ({ first_name, last_name, email, password_hash }) => {
  const query = `
    INSERT INTO Users (first_name, last_name, email, password_hash)
    VALUES ($1, $2, $3, $4)
  `;
  return await pool.query(query, [first_name, last_name, email, password_hash]);
};

export const fetchAllProfiles = async () => {
  const result = await pool.query('SELECT * FROM Users');
  return result.rows;
};

export const findUserById = async (id) => {
  const result = await pool.query('SELECT * FROM Users WHERE id = $1', [id]);
  return result.rows[0];
};

export const updateProfileById = async (id, data) => {
  const fields = Object.keys(data);
  const values = Object.values(data);
  const setClause = fields.map((f, i) => `${f} = $${i + 1}`).join(', ');
  const result = await pool.query(
    `UPDATE Users SET ${setClause} WHERE id = $${fields.length + 1} RETURNING *`,
    [...values, id]
  );
  return result.rows[0];
};

export const deleteProfileById = async (id) => {
  await pool.query('DELETE FROM Users WHERE id = $1', [id]);
};

export const findUserByEmail = async (email) => {
  const result = await pool.query('SELECT * FROM Users WHERE email = $1', [email]);
  return result.rows[0];
};
```
## Контролери для MediaContent
```

import handleAsync from '../utils/handleAsync.js';
import {
  insertMediaContent,
  getAllMediaContents,
  getMediaContentById,
  updateMediaContentById,
  deleteMediaContentById,
} from '../models/mediaContentModel.js';
import AppError from '../utils/appError.js';
import { validateRequiredContentFields } from '../utils/validator.js';

export const createMediaContent = handleAsync(async (req, res) => {
  const contentData = req.body;
  validateRequiredContentFields(contentData);
  const newContent = await insertMediaContent(contentData);
  res.status(201).json({ status: 'success', data: newContent });
});

export const getMediaContents = handleAsync(async (req, res) => {
  const contents = await getAllMediaContents();
  res.status(200).json({ status: 'success', data: contents });
});

export const getMediaContent = handleAsync(async (req, res) => {
  const { id } = req.params;
  const content = await getMediaContentById(id);
  if (!content) {
    throw new AppError('MediaContentNotFoundException', 404);
  }
  res.status(200).json({ status: 'success', data: content });
});

export const updateMediaContent = handleAsync(async (req, res) => {
  const { id } = req.params;
  const updates = req.body;
  const content = await getMediaContentById(id);
  if (!content) {
    throw new AppError('MediaContentNotFoundException', 404);
  }
  const updated = await updateMediaContentById(id, updates);
  res.status(200).json({ status: 'success', data: updated });
});

export const deleteMediaContent = handleAsync(async (req, res) => {
  const { id } = req.params;
  const deleted = await deleteMediaContentById(id);
  if (!deleted) {
    throw new AppError('MediaContentNotFoundException', 404);
  }
  res.status(200).json({ status: 'success', message: 'Media content deleted successfully' });
});
```
## Взаємодія з базою даних для MediaContent
```
import pool from '../db.js';
import AppError from '../utils/appError.js';

export const insertMediaContent = async ({
  title,
  description,
  body,
  content_type,
  user_id,
}) => {
  const result = await pool.query(
    `INSERT INTO MediaContent (title, description, body, content_type, user_id)
     VALUES ($1, $2, $3, $4, $5) RETURNING *`,
    [title, description, body, content_type, user_id]
  );
  return result.rows[0];
};

export const getAllMediaContents = async () => {
  const result = await pool.query('SELECT * FROM MediaContent');
  return result.rows;
};

export const getMediaContentById = async (id) => {
  const result = await pool.query('SELECT * FROM MediaContent WHERE id = $1', [id]);
  return result.rows[0] || null;
};

export const updateMediaContentById = async (id, data) => {
  const fields = Object.keys(data);
  const values = Object.values(data);
  if (!fields.length) {
    throw new AppError('NoFieldsToUpdateException', 400);
  }
  const setClause = fields.map((f, i) => `${f} = $${i + 1}`).join(', ');
  const result = await pool.query(
    `UPDATE MediaContent SET ${setClause} WHERE id = $${fields.length + 1} RETURNING *`,
    [...values, id]
  );
  return result.rows[0];
};

export const deleteMediaContentById = async (id) => {
  const result = await pool.query(
    'DELETE FROM MediaContent WHERE id = $1 RETURNING *',
    [id]
  );
  return result.rows[0] || null;
};
```
## Мідлвар для обробки помилок
```
const errorHandler = (err, req, res, next) => {
  console.error(err);
  err.statusCode = err.statusCode || 500;
  err.status = err.status || 'error';
  res.status(err.statusCode).json({ status: err.status, message: err.message });
};

export default errorHandler;
```
## Обгортка над функціями для перенаправлення помилок
```

const handleAsync = (fn) => (req, res, next) => {
  fn(req, res, next).catch(next);
};

export default handleAsync;
```
## Валідатори для перевірки вхідних даних
```

import AppError from './appError.js';

export const validateRequiredFields = ({
  first_name,
  last_name,
  email,
  password_hash,
}) => {
  if (!first_name || !last_name || !email || !password_hash) {
    throw new AppError('DataMissingException', 400);
  }
};

export const validateRequiredContentFields = ({
  title,
  body,
  content_type,
  user_id,
}) => {
  if (!title || !body || !content_type || !user_id) {
    throw new AppError('RequiredFieldsMissingException', 400);
  }
};
```
## Модифікований клас помилки
```

export default class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error';
    Error.captureStackTrace(this, this.constructor);
  }
}
```
