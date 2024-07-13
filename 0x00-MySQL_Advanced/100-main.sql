-- Show initial data
SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM corrections;

-- Compute average weighted score for Jeanne
CALL ComputeAverageWeightedScoreForUser((SELECT id FROM users WHERE name = "Jeanne"));

-- Show updated data
SELECT "--";
SELECT * FROM users;
