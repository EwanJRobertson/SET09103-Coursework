DROP TABLE IF EXISTS issues;
DROP TABLE IF EXISTS projects_users_link;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS projects;

CREATE TABLE projects (
    project_id int NOT NULL,
    title text NOT NULL,
    version text NOT NULL,
    PRIMARY KEY(project_id)
);

CREATE TABLE users (
    user_id int NOT NULL,
    username text NOT NULL,
    password_hash text NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE projects_users_link (
    project_id int NOT NULL,
    user_id int NOT NULL,
    FOREIGN KEY(project_id) REFERENCES projects(project_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE issues (
    project_id int NOT NULL,
    issue_id int NOT NULL,
    title text NOT NULL,
    description text,
    type_of_issue text NOT NULL,
    date_created datetime NOT NULL,
    version_introduced text,
    user_id int,
    priority_level int,
    status int NOT NULL,
    PRIMARY KEY(project_id, issue_id),
    FOREIGN KEY(user_id) REFERENCES projects_users_link(user_id)
);