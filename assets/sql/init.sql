/*# This is free software licensed under the MIT license.
# Copyright (c) 2021 Samarth Ramesh <samarthr1@outlook.com>
 You should have recived a copy of the MIT license with this file. In case you ahve not, visit https://github.com/samarth-ramsh/mtlaucher
*/

CREATE TABLE users ( username VARCHAR(20) UNIQUE, passwd VARCHAR(256));
CREATE TABLE passwds (addr VARCHAR, port INT, uname VARCHAR, passwd BLOB, iv BLOB);