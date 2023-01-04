-- view №1
CREATE VIEW count_authors_by_country AS 
SELECT TRIM(auth_country), COUNT(auth_id) FROM authors group by auth_country; 

-- view №2
CREATE VIEW count_podcast_by_language AS 
SELECT podc_language, COUNT(podc_id) FROM podcasts group by podc_language;


-- view №3
CREATE VIEW count_podcast_by_duration AS 
SELECT TRIM(podc_title), SUM(ep_audio_lenth) AS total_duration FROM podcasts, episodes
WHERE episodes.podc_id = podcasts.podc_id 
group by podc_title ORDER BY total_duration DESC;

