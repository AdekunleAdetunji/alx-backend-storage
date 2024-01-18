-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student. Note: An average score can be a decimal
-- Requirements:
    -- Procedure ComputeAverageScoreForUser is taking 1 input:
    -- user_id, a users.id value (you can assume user_id is linked to an existing users)
DELIMITER $$ ;
CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
BEGIN
    UPDATE users
    SET average_score = (SELECT AVG(score) FROM corrections
                WHERE user_id=corrections.user_id);
END;$$
DELIMITER ;