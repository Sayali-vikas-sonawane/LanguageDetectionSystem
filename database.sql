create database userLogin;
use userLogin;

create table userInfo(uid varchar(30) primary key not null, pass varchar(30) not null);
desc userInfo;

select *from userInfo;
create table resgiterUser(fname varchar(20), lname varchar(20), contact varchar(30), age int , gender varchar(10), bg varchar(5), city varchar(30),
email varchar(30) not null primary key);

desc resgiterUser;
select * from resgiterUser;