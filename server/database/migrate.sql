drop table if exists games;
drop table if exists users;

PRAGMA foreign_keys = on;

create table users(
    id integer primary key autoincrement not null,
    username text not null,
    balance float default 100.0,
    password text not null,
    session text 
);


create table games(
    id integer primary key autoincrement not null,
    gameSession integer not null,
    playerCards text not null, 
    dealerCards text not null,
    bet float not null,
    outcome text default null
);