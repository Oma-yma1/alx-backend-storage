-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users AS Us,
        (SELECT Us.id, SUM(score * weight) / SUM(weight) AS w_avg
        FROM users AS Us
        JOIN corrections as Co ON Us.id=Co.user_id
        JOIN projects AS Pr ON Co.project_id=Pr.id
        GROUP BY Us.id)
    AS WAt
    SET Us.average_score = WAt.w_avg
    WHERE Us.id=WAt.id;
END
//
DELIMITER ;
