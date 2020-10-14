CREATE TABLE USERS (
    id serial primary key,
    api_key varchar(100) unique not null,
    username varchar not null ,
    password varchar not null
);

INSERT INTO
    USERS(api_key, username, password)
VALUES (
        'GPN.55a00773b4c774219deea743b1e72c49cbb411ab.bd11fd1ae2dad2c1155fb7957ab7eb7a8aa88aa5',
        'KHAYUROV',
        '41a8238e848237e9e17e9f7ba32bcac7ecb5ab2a674bbdc3d092fd43a753273ed30f170923e9a1669cc67043aad703489577dd644fc48a5e3a189ad1899c475a'
);
