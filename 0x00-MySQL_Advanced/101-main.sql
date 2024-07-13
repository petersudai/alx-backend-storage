-- Show initial data
SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM corrections;

-- Compute average weighted score for all users
CALL ComputeAverageWeightedScoreForUsers();

-- Show updated data
SELECT "--";
SELECT * FROM users;
