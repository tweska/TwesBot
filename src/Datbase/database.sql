create type chat_type as enum ('private', 'group', 'supergroup', 'channel')
;

create table chat
(
	chat_id integer not null
		constraint chat_pkey
			primary key,
	type chat_type not null,
	title varchar(128)
)
;

create table "user"
(
	user_id integer not null
		constraint user_pkey
			primary key,
	first_name varchar(32) not null,
	last_name varchar(32),
	username varchar(32)
)
;

create table chat_member
(
	user_id integer
		constraint chat_member_user_user_id_fk
			references "user"
				on update cascade on delete cascade,
	chat_id integer not null
		constraint chat_member_chat_id_pk
			primary key
		constraint chat_member_chat_chat_id_fk
			references chat
				on update cascade on delete cascade
)
;

create table message
(
	message_id integer not null
		constraint message_pkey
			primary key,
	"from" integer,
	chat integer not null,
	date timestamp not null,
	content text not null
)
;

create function add_message(message_id integer, date timestamp without time zone, content text, user_id integer, first_name character varying, last_name character varying, username character varying, chat_id integer, type chat_type, title character varying) returns void
	language plpgsql
as $$
BEGIN
  INSERT INTO "user"
  VALUES (user_id, first_name, last_name, username)
  ON CONFLICT DO NOTHING;

  INSERT INTO chat
  VALUES (chat_id, type, title)
  ON CONFLICT DO NOTHING;

  INSERT INTO chat_member
  VALUES (user_id, chat_id)
  ON CONFLICT DO NOTHING;

  INSERT INTO message
  VALUES (message_id, user_id, chat_id, date, content);
END;
$$
;
