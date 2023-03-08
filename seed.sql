TRUNCATE TABLE users CASCADE;

INSERT INTO users (name, email, password, created_at, updated_at)
VALUES ('shiam', 'shiamuddulla29@hotmail.com', 'Portugal79', NOW(), NOW());

TRUNCATE TABLE anime CASCADE;

INSERT INTO anime (id, name, year, image_url)
VALUES (1, 'naruto shippuden', 2007, 'http://cdn.shopify.com/s/files/1/0024/9803/5810/products/556692-Product-0-I-637750956758954003_1024x1024.jpg');

INSERT INTO anime (id, name, year, image_url)
VALUES (2, 'demon slayer', 2019, 'https://m.mediaamazon.com/images/M/MV5BZjZjNzI5MDctY2Y4YS00NmM4LTljMmItZTFkOTExNGI3ODRhXkEyXkFqcGdeQXVyNjc3MjQzNTI@._V1_.jpg');

INSERT INTO anime (id, name, year, image_url)
VALUES (3, 'jujutsu kaisen', 2020, 'https://static.wikia.nocookie.net/jujutsu-kaisen/images/8/88/Anime_Key_Visual_2.png/revision/latest?cb=20201212034001');
