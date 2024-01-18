-- SQL script that creates a function SafeDiv

DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv (a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    DECLARE num FLOAT DEFAULT 0;

    IF b != 0 THEN
        SET num = a / b;
    END IF;
    RETURN num;
END $$
DELIMITER ;
