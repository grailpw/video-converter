CREATE TABLE IF NOT EXISTS videos (
	id serial primary key,
	name varchar(200) not null,
	descr text
)

INSERT INTO videos(name, descr) VALUES('{data[title]}', '{data[desc]}');

select * from videos