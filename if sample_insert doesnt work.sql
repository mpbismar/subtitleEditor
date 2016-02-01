use sub_db;
alter table video_video drop column pub_date;
alter table video_video add pub_date datetime default current_timestamp;
alter table video_sequence drop column pub_date;
alter table video_sequence add pub_date datetime default current_timestamp;
