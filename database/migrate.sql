drop table if exists transactions;
drop table if exists users;

PRAGMA foreign_keys = on;

create table users(
    id integer primary key autoincrement not null,
    firstname text not null,
    lastname text not null,
    email text not null,
    username text not null,
    password text not null
);


create table transactions(
    id integer primary key autoincrement not null,
    userId integer not null,
    time datetime not null default CURRENT_TIMESTAMP,
    value text not null,
    foreign key (userId) references users(id)
);
