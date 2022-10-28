SELECT
	i.image_id,
	i.file_name,
	i.image_type,
	q.quality,
	c.x,
	c.y,
	c.z
FROM
	2022_tomocube_sepsis_image i
	LEFT JOIN `2022_tomocube_sepsis_image_quality` q ON i.image_id = q.image_id
	LEFT JOIN `2022_tomocube_sepsis_image_center` c ON i.image_id = c.image_id
WHERE x IS NOT NULL AND y IS NOT NULL AND z IS NOT NULL