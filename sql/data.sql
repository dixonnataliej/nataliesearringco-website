INSERT INTO posts(postid, filename, name, price, description, status)
VALUES (1, 'rainbow_earrings_2948.jpg', 'Rainbow Star Earrings', '$10',
        'These sure' || ' are rainbow star earrings', 'Made to Order'),
       (2, 'blue_earrings_purple_12y87.jpg', 'Blue Purple Circles', '$10',
       'description pending', 'Available'),
       (3, 'pastel_butterfly_esque_earrings_2389.jpg',
        'Pastel Butterfly Esque' ||
       ' Earrings', '$15', 'description tbd', 'Sold Out');

INSERT INTO tags(tagid, name)
VALUES (1, '$10 or less'),
       (2, 'pride');

INSERT INTO post_tags(postid, tagid)
VALUES (1, 1),
       (1, 2),
       (2, 1);