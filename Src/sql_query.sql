
SELECT 
    Subject,
    COUNT(*) AS Count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS Percentage,
FROM learned_material
GROUP BY Subject
ORDER BY Count DESC
