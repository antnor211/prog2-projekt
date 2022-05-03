drop table if exists games;
drop table if exists users;

PRAGMA foreign_keys = on;

create table users(
    id integer primary key autoincrement not null,
    firstname text not null,
    lastname text not null,
    username text not null,
    balance float default null,
    password text not null
);


create table games(
    id integer primary key not null,
    gameSession integer not null,
    playerCards text not null, 
    dealerCards text not null
);