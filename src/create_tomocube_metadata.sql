SELECT
	i.image_id,
	i.file_name,
	i.image_type,
	q.quality,
	c.x,
	c.y,
	c.z
FROM
	PROJECT_image i
	LEFT JOIN `PROJECT_image_quality` q ON i.image_id = q.image_id
	LEFT JOIN `PROJECT_image_center` c ON i.image_id = c.image_id
WHERE x IS NOT NULL AND y IS NOT NULL AND z IS NOT NULL