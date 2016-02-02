use sub_db;
/*DELETE FROM video_video WHERE vid < 0;
DELETE FROM video_sequence WHERE sid < 0;
INSERT INTO video_video (name,lang,sub_langs) VALUES ("flat-animation","en","en,de");
INSERT INTO video_video (name,lang,sub_langs) VALUES ("Sample-Video-1","en","en,de");*/
insert into video_user (name,password) values ("admin","Manager1");
insert into video_sequence (vid_id,lang, content,start,end,creator_id,rating) values (1,"en", "english",100,2000,1,0);
insert into video_sequence (vid_id,lang, content,start,end,creator_id,rating) values (1,"en", "Hey, bla, bla",2100,4000,1,0);
insert into video_sequence (vid_id,lang, content,start,end,creator_id,rating) values (1,"en", "Hey, bla, bla",4100,6000,1,0);
insert into video_sequence (vid_id,lang, content,start,end,creator_id,rating) values (1,"de", "deutsch",100,2000,1,0);
insert into video_sequence (vid_id,lang, content,start,end,creator_id,rating) values (1,"de", "Hey, bla, bla",2100,4000,1,0);
insert into video_sequence (vid_id,lang, content,start,end,creator_id,rating) values (1,"de", "Hey, bla, bla",4100,6000,1,0);
insert into video_sequence (vid_id,lang, content,start,end,creator_id,rating) values (2,"en", "english",100,2000,1,0);
insert into video_sequence (vid_id,lang, content,start,end,creator_id,rating) values (2,"en", "Hey, bla, bla",2100,4000,1,0);
insert into video_sequence (vid_id,lang, content,start,end,creator_id,rating) values (2,"en", "Hey, bla, bla",4100,6000,1,0);
insert into video_sequence (vid_id,lang, content,start,end,creator_id,rating) values (2,"de", "deutsch",100,2000,1,0);
insert into video_sequence (vid_id,lang, content,start,end,creator_id,rating) values (2,"de", "Hey, bla, bla",2100,4000,1,0);
insert into video_sequence (vid_id,lang, content,start,end,creator_id,rating) values (2,"de", "Hey, bla, bla",4100,6000,1,0);
