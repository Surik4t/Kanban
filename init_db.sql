CREATE TABLE boards (
  id UUID PRIMARY KEY,
  title VARCHAR,
  description VARCHAR,
  "user" VARCHAR
);

CREATE TABLE columns (
  pos INTEGER,
  uuid UUID,
  title VARCHAR(30),
  board_id UUID
);

CREATE TABLE cards (
  id UUID,
  column_id UUID,
  priority VARCHAR,
  header VARCHAR,
  text VARCHAR,
  card_index INTEGER
);

CREATE TABLE users (
  username VARCHAR(16) UNIQUE,
  password VARCHAR,
  bio VARCHAR(260),
  mail VARCHAR(60),
  phone VARCHAR(20)
);

CREATE TABLE expired_tokens (
  jti UUID PRIMARY KEY
);