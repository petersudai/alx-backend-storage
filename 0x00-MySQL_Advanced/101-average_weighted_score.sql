-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;
    DECLARE weight_sum FLOAT;
    DECLARE weighted_sum FLOAT;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Calculate the weighted sum and the sum of weights for the user
        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO weighted_sum, weight_sum
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Update the average score for the user
        IF weight_sum > 0 THEN
            UPDATE users
            SET average_score = weighted_sum / weight_sum
            WHERE id = user_id;
        ELSE
            UPDATE users
            SET average_score = 0
            WHERE id = user_id;
        END IF;
    END LOOP;

    CLOSE cur;
END //

DELIMITER ;
