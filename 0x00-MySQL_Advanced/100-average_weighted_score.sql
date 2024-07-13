-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE weighted_sum FLOAT;
    DECLARE total_weight INT;

    -- Calculate the weighted sum of the scores
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO weighted_sum, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Update the user's average score
    UPDATE users
    SET average_score = IF(total_weight = 0, 0, weighted_sum / total_weight)
    WHERE id = user_id;
END //

DELIMITER ;
