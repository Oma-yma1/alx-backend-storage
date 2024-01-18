-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER |
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  UPDATE users AS Us, 
    (SELECT Us.id, SUM(score * weight) / SUM(weight) AS we_avg 
    FROM users AS Us 
    JOIN corrections as Co ON U.id=C.user_id 
    JOIN projects AS Pp ON Co.project_id=Pp.id 
    GROUP BY Us.id)
  AS WAt
  SET Us.average_score = WAt.we_avg 
  WHERE Us.id=WAt.id;
END;
