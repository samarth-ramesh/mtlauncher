CREATE TABLE users ( username VARCHAR(20) UNIQUE, passwd VARCHAR(256));
CREATE TABLE passwds (addr VARCHAR, port INT, uname VARCHAR, passwd BLOB, iv BLOB);
CREATE TABLE history(addr VARCHAR, port INT, uname VARCHAR, timeAt VARCHAR);