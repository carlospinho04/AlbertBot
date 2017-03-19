DROP TABLE account;
CREATE TABLE account(
  user_id serial PRIMARY KEY,
  username VARCHAR (50) UNIQUE NOT NULL,
  password VARCHAR (50) NOT NULL,
  name VARCHAR (50),
  phone_number integer
);
