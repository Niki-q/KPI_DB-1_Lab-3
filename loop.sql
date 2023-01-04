
DO $$
 DECLARE
     podc_id   podcasts.podc_id%TYPE;
     auth_id podcasts.auth_id%TYPE;

 BEGIN
     podc_id := 20000000;
     auth_id := 5775700;
     FOR counter IN 58..63
         LOOP
            INSERT INTO podcasts (podc_id, auth_id, podc_language)
             VALUES (CAST (podc_id AS INT) + counter, counter + CAST (auth_id AS INT), 'Ukrainian');
         END LOOP;
 END;
 $$






