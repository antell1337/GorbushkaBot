create table product
(
    id SERIAL PRIMARY KEY ,
    name varchar(100) null
);

create table iPhoneColor
(
    id SERIAL PRIMARY KEY,
    name varchar(100) not null
);

create table iPhoneColorConnection
(
    id SERIAL PRIMARY KEY,
    modelId int not null,
    paramId int not null
);

create table iPhoneCountry
(
    id SERIAL PRIMARY KEY,
    name varchar(100) not null
);

create table iPhoneCountryConnection
(
    id SERIAL PRIMARY KEY,
    modelId int not null,
    paramId int not null
);

create table iPhoneMemory
(
    id SERIAL PRIMARY KEY,
    name varchar(100) not null
);

create table iPhoneMemoryConnection
(
    id SERIAL PRIMARY KEY,
    modelId int not null,
    paramId int not null
);

create table iPhoneOffer
(
    id SERIAL PRIMARY KEY,
    model   varchar(100) not null,
    Memory  varchar(100) null,
    Color   varchar(100) null,
    Country varchar(100) null,
    price   varchar(100) not null,
    "user"    varchar(100) not null
);

create table model
(
    id SERIAL PRIMARY KEY,
    productId int          not null,
    name      varchar(100) null,
    paramsStr varchar(100) null
);

create table SamsungColor
(
    id SERIAL PRIMARY KEY,
    name varchar(100) not null
);

create table SamsungColorConnection
(
    id SERIAL PRIMARY KEY,
    modelId int not null,
    paramId int not null
);

create table SamsungCountry
(
    id SERIAL PRIMARY KEY,
    name varchar(100) not null
);

create table SamsungCountryConnection
(
    id SERIAL PRIMARY KEY,
    modelId int not null,
    paramId int not null
);

create table SamsungMemory
(
    id SERIAL PRIMARY KEY,
    name varchar(100) not null
);

create table SamsungMemoryConnection
(
    id SERIAL PRIMARY KEY,
    modelId int not null,
    paramId int not null
);

create table SamsungOffer
(
    id SERIAL PRIMARY KEY,
    model   varchar(100) not null,
    Memory  varchar(100) null,
    Color   varchar(100) null,
    Country varchar(100) null,
    price   varchar(100) not null,
    "user"    varchar(100) not null
);

create table Users
(
    id SERIAL PRIMARY KEY,
    user_id  varchar(100) null,
    nickname varchar(100) null,
    chat_id  varchar(100) null
);