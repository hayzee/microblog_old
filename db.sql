drop table followers;
drop table posts;
drop table users;

  CREATE TABLE "MEGA"."USERS" 
   (	"ID" INTEGER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL ENABLE, 
	"USERNAME" VARCHAR2(64 CHAR), 
	"EMAIL" VARCHAR2(120 CHAR), 
	"PASSWORD_HASH" VARCHAR2(128 CHAR), 
    about_me varchar2(140)
	 PRIMARY KEY ("ID")
   ) ;

  CREATE UNIQUE INDEX "MEGA"."ix_USERS_email" ON "MEGA"."USERS" ("EMAIL");

  CREATE UNIQUE INDEX "MEGA"."ix_USERS_username" ON "MEGA"."USERS" ("USERNAME"); 


  CREATE TABLE "MEGA"."POSTS" 
   ("ID" INTEGER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) NOT NULL ENABLE, 
	"BODY" VARCHAR2(140 CHAR), 
	"TIMESTAMP" DATE, 
	"USER_ID" NUMBER(*,0) references users, 
	 PRIMARY KEY ("ID")
   );
   
  CREATE INDEX "MEGA"."ix_POSTS_timestamp" ON "MEGA"."POSTS" ("TIMESTAMP") ;


  CREATE TABLE "MEGA"."FOLLOWERS" 
   ("FOLLOWER_ID" NUMBER(*,0), 
	"FOLLOWED_ID" NUMBER(*,0), 
	 FOREIGN KEY ("FOLLOWER_ID")
	  REFERENCES "MEGA"."USERS" ("ID") ENABLE, 
	 FOREIGN KEY ("FOLLOWED_ID")
	  REFERENCES "MEGA"."USERS" ("ID") ENABLE
   );


TRUNCATE TABLE USERS;


select * from posts order by 1;

alter table users add (about_me varchar2(140), last_seen date default sysdate);

alter table posts
modify (
"BODY" not null);

alter table posts
modify (
"TIMESTAMP" not null );

alter table posts
modify (
"TIMESTAMP" default null);

alter table posts
modify (
"USER_ID" not null);

create table sausage(sausage_id integer primary key);

drop table sausage;


delete from followers;
delete from posts;
delete from users;
