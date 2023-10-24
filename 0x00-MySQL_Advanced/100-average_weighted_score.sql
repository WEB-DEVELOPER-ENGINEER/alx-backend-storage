-- a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(user_id INT)
BEGIN
    UPDATE users AS U
    JOIN corrections AS C ON U.id = C.user_id
    JOIN projects AS P ON C.project_id = P.id
    WHERE U.id = user_id;
    SET U.average_score = COALESCE(SUM(C.score * P.weight) / SUM(P.weight), 0)
END
$$
DELIMITER ;
