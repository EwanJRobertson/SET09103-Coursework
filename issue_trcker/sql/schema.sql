DROP TABLE IF EXISTS issues;
DROP TABLE IF EXISTS users_projects_link;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS projects;

CREATE TABLE projects (
    project_id int NOT NULL,
    title text NOT NULL,
    version text NOT NULL,
    PRIMARY KEY(project_id)
);

CREATE TABLE users (
    username text NOT NULL,
    password_hash text NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE users_projects_link (
    username text NOT NULL,
    project_id int NOT NULL,
    PRIMARY KEY(project_id, username),
    FOREIGN KEY(project_id) REFERENCES projects(project_id),
    FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE issues (
    project_id int NOT NULL,
    issue_id int NOT NULL,
    title text NOT NULL,
    description text,
    type_of_issue text NOT NULL,
    date_last_updated datetime NOT NULL,
    version_introduced text,
    username text,
    priority_level int,
    status text NOT NULL,
    PRIMARY KEY(project_id, issue_id),
    FOREIGN KEY(username) REFERENCES users_projects_link(username)
);
