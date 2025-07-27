-- Tabla que almacena la información de las películas
create table public.imdb_movies (
  movie_id text not null, -- ID único de la película
  title text null, -- Título de la película
  year integer null, -- Año de lanzamiento
  rating double precision null, -- Calificación promedio
  duration integer null, -- Duración en minutos
  metascore integer null, -- Puntuación Metascore
  created_at timestamp without time zone null default CURRENT_TIMESTAMP, -- Fecha de inserción
  constraint imdb_movies_pkey primary key (movie_id) -- Clave primaria
) TABLESPACE pg_default;

-- Tabla que almacena la relación entre actores y películas
create table public.imdb_actors (
  actor_id text not null, -- ID único del actor
  movie_id text not null, -- ID único de la película
  name text null, -- Nombre del actor
  is_main_character boolean null, -- Indica si es personaje principal
  created_at timestamp without time zone null default CURRENT_TIMESTAMP, -- Fecha de inserción
  constraint imdb_actors_pkey primary key (actor_id, movie_id) -- Clave primaria compuesta
) TABLESPACE pg_default;




-- Solución a preguntas propuestas en el documento

--------------------------------------------------------------------------
-- 1. Obtener las 5 películas con mayor promedio de duración por década. -
--------------------------------------------------------------------------

WITH movies_by_decade AS (
    SELECT
        movie_id,
        title,
        year,
        duration,
        (year / 10) * 10 AS decade  -- Calculamos la década
    FROM imdb_movies
),
ranked_movies AS (
    SELECT
        decade,
        title,
        duration,
        RANK() OVER (PARTITION BY decade ORDER BY duration DESC) AS rank_in_decade
    FROM movies_by_decade
)
SELECT
    decade,
    title,
    duration
FROM ranked_movies
WHERE rank_in_decade <= 5
ORDER BY decade, duration DESC;

--                               RESULTS

-- No se muestra mas en 1930 por ejemplo por que no agrege solo agregue 50 peliculas 

-- | decade | title                                             | duration |
-- | ------ | ------------------------------------------------- | -------- |
-- | 1930   | Modern Times                                      | 87       |
-- | 1940   | It's a Wonderful Life                             | 130      |
-- | 1940   | Casablanca                                        | 102      |
-- | 1950   | Shichinin no samurai                              | 207      |
-- | 1950   | 12 Angry Men                                      | 96       |
-- | 1960   | Il buono, il brutto, il cattivo                   | 182      |
-- | 1960   | Seppuku                                           | 133      |
-- | 1960   | Psycho                                            | 109      |
-- | 1970   | The Godfather Part II                             | 202      |
-- | 1970   | The Godfather                                     | 175      |
-- | 1970   | One Flew Over the Cuckoo's Nest                   | 133      |
-- | 1970   | Star Wars                                         | 121      |
-- | 1970   | Alien                                             | 117      |
-- | 1980   | Nuovo Cinema Paradiso                             | 174      |
-- | 1980   | Star Wars: Episode V - The Empire Strikes Back    | 124      |
-- | 1980   | Back to the Future                                | 116      |
-- | 1990   | Schindler's List                                  | 195      |
-- | 1990   | Saving Private Ryan                               | 169      |
-- | 1990   | Pulp Fiction                                      | 154      |
-- | 1990   | GoodFellas                                        | 145      |
-- | 1990   | The Shawshank Redemption                          | 142      |
-- | 1990   | Forrest Gump                                      | 142      |
-- | 2000   | The Lord of the Rings: The Return of the King     | 201      |
-- | 2000   | The Green Mile                                    | 189      |
-- | 2000   | The Lord of the Rings: The Two Towers             | 179      |
-- | 2000   | The Lord of the Rings: The Fellowship of the Ring | 178      |
-- | 2000   | Gladiator                                         | 155      |
-- | 2010   | Interstellar                                      | 169      |
-- | 2010   | Inception                                         | 148      |
-- | 2010   | Gisaengchung                                      | 132      |
-- | 2010   | Intouchables                                      | 112      |
-- | 2010   | Whiplash                                          | 106      |
-- | 2020   | Spider-Man: Across the Spider-Verse               | 140      |





----------------------------------------------------------------------
-- 2. Calcular la desviación estándar de las calificaciones por año. -
----------------------------------------------------------------------

SELECT 
    year,
    AVG(rating) AS promedio_rating,
    STDDEV_POP(rating) AS desviacion_estandar
FROM imdb_movies
GROUP BY year
ORDER BY year;

--                 RESULTS

-- | year | promedio_rating  | desviacion_estandar |
-- | ---- | ---------------- | ------------------- |
-- | 1936 | 8.5              | 0                   |
-- | 1943 | 8.5              | 0                   |
--                   ...
-- | 1979 | 8.5              | 0                   |
-- | 1980 | 8.7              | 0                   |
-- | 1985 | 8.5              | 0                   |
-- | 1989 | 8.5              | 0                   |
-- | 1990 | 8.6              | 0.0999999999999996  |
-- | 1991 | 8.6              | 0                   |
-- | 1994 | 8.76666666666667 | 0.205480466765633   |
-- | 1995 | 8.775            | 0.326917420765551   |
-- | 1996 | 8.6              | 0                   |
-- | 1998 | 8.6              | 0                   |
-- | 1999 | 8.65             | 0.11180339887499    |
-- | 2000 | 8.55             | 0.0499999999999989  |
-- | 2001 | 8.9              | 0                   |
-- | 2002 | 8.63333333333333 | 0.124721912892465   |
-- | 2003 | 8.8              | 0.200000000000001   |
-- | 2006 | 8.5              | 0                   |
-- | 2007 | 8.5              | 0                   |
--                  ...
-- | 2015 | 8.5              | 0                   |
-- | 2019 | 8.5              | 0                   |
-- | 2023 | 8.5              | 0                   |




-------------------------------------------------------------------------------------------------------------
-- 3. Detectar películas con más de un 20% de diferencia entre calificación IMDB y Metascore (normalizado). -
-------------------------------------------------------------------------------------------------------------

SELECT 
    movie_id,
    title,
    year,
    rating AS imdb_rating,
    metascore,
    (metascore / 10.0)::numeric(4,2) AS metascore_normalized,
    ABS(rating - (metascore / 10.0)) AS difference,
    ABS(rating - (metascore / 10.0)) * 10 AS diferencia_pct
FROM imdb_movies
WHERE metascore IS NOT NULL
  AND rating IS NOT NULL
  AND ABS(rating - (metascore / 10.0)) > 2
ORDER BY diferencia_pct DESC;



--                 RESULTS


-- | movie_id  | title              | year | imdb_rating | metascore | metascore_normalized | difference | diferencia_pct |
-- | --------- | ------------------ | ---- | ----------- | --------- | -------------------- | ---------- | -------------- |
-- | tt0118799 | La vita è bella    | 1999 | 8.6         | 58        | 5.80                 | 2.8        | 28             |
-- | tt1675434 | Intouchables       | 2012 | 8.5         | 57        | 5.70                 | 2.8        | 28             |
-- | tt0120689 | The Green Mile     | 2000 | 8.6         | 61        | 6.10                 | 2.5        | 25             |
-- | tt0120586 | American History X | 1999 | 8.5         | 62        | 6.20                 | 2.3        | 23             |
-- | tt0137523 | Fight Club         | 1999 | 8.8         | 67        | 6.70                 | 2.1        | 21             |
-- | tt0110413 | Léon               | 1995 | 8.5         | 64        | 6.40                 | 2.1        | 21             |
-- | tt0114369 | Se7en              | 1996 | 8.6         | 65        | 6.50                 | 2.1        | 21             |



-----------------------------------------------------------------------------------------------------
-- 4. Crear una vista que relacione películas y actores, y permita filtrar por actor principal.     -
-----------------------------------------------------------------------------------------------------


CREATE OR REPLACE VIEW movie_actor_view AS
SELECT 
    m.movie_id,
    m.title,
    m.year,
    m.rating,
    m.duration,
    a.actor_id,
    a.name AS actor_name,
    a.is_main_character
FROM imdb_movies m
JOIN imdb_actors a 
  ON m.movie_id = a.movie_id;


--                 RESULTS

--    EJEMPLO DE CONSULTA A LA VISTA

SELECT *
FROM movie_actor_view
WHERE is_main_character = TRUE;


-- | movie_id  | title                                          | year | rating | duration | actor_id  | actor_name               | is_main_character |
-- | --------- | ---------------------------------------------- | ---- | ------ | -------- | --------- | ------------------------ | ----------------- |
-- | tt1375666 | Inception                                      | 2010 | 8.8    | 148      | nm0000138 | Leonardo DiCaprio        | true              |
-- | tt1375666 | Inception                                      | 2010 | 8.8    | 148      | nm0330687 | Joseph Gordon-Levitt     | true              |
-- | tt1375666 | Inception                                      | 2010 | 8.8    | 148      | nm0680983 | Elliot Page              | true              |
-- | tt1375666 | Inception                                      | 2010 | 8.8    | 148      | nm0362766 | Tom Hardy                | true              |
-- | tt0120815 | Saving Private Ryan                            | 1998 | 8.6    | 169      | nm0000158 | Tom Hanks                | true              |
-- | tt0816692 | Interstellar                                   | 2014 | 8.7    | 169      | nm0000190 | Matthew McConaughey      | true              |
-- | tt0080684 | Star Wars: Episode V - The Empire Strikes Back | 1980 | 8.7    | 124      | nm0000434 | Mark Hamill              | true              |
-- | tt0137523 | Fight Club                                     | 1999 | 8.8    | 139      | nm0000093 | Brad Pitt                | true              |
-- | tt0133093 | The Matrix                                     | 1999 | 8.7    | 136      | nm0000206 | Keanu Reeves             | true              |
-- | tt0027977 | Modern Times                                   | 1936 | 8.5    | 87       | nm0000122 | Charles Chaplin          | true              |
-- | tt0120815 | Saving Private Ryan                            | 1998 | 8.6    | 169      | nm0001744 | Tom Sizemore             | true              |
-- | tt0120815 | Saving Private Ryan                            | 1998 | 8.6    | 169      | nm0122653 | Edward Burns             | true              |
-- | tt0120815 | Saving Private Ryan                            | 1998 | 8.6    | 169      | nm0001608 | Barry Pepper             | true              |
-- | tt0073486 | One Flew Over the Cuckoo's Nest                | 1976 | 8.7    | 133      | nm0077720 | Michael Berryman         | true              |
-- | tt0073486 | One Flew Over the Cuckoo's Nest                | 1976 | 8.7    | 133      | nm0110480 | Peter Brocco             | true              |
-- | tt0073486 | One Flew Over the Cuckoo's Nest                | 1976 | 8.7    | 133      | nm0111954 | Dean R. Brooks           | true              |


SELECT *
FROM movie_actor_view
WHERE actor_name = 'Leonardo DiCaprio'
  AND is_main_character = TRUE;


-- | movie_id  | title        | year | rating | duration | actor_id  | actor_name        | is_main_character |
-- | --------- | ------------ | ---- | ------ | -------- | --------- | ----------------- | ----------------- |
-- | tt1375666 | Inception    | 2010 | 8.8    | 148      | nm0000138 | Leonardo DiCaprio | true              |
-- | tt0407887 | The Departed | 2006 | 8.5    | 151      | nm0000138 | Leonardo DiCaprio | true              |



------------------------------------------------------------------------------------------
-- 5. Crear un índice o partición si se justifica para consultas frecuentes.             -
------------------------------------------------------------------------------------------

-- Para crear un indice en la tabla imdb_movies, con los datos actuales no es necesario,
-- pero si se espera que la tabla crezca significativamente, un índice en el año puede ser útil.

CREATE INDEX idx_movies_year ON imdb_movies(year);


-- Modificar la tabla imdb_movies para particionarla por año
ALTER TABLE imdb_movies
PARTITION BY RANGE (year);

-- Crear particiones por décadas, sin embargo para la cantidad de datos actual no es necesario y puede ralentizar más los resultados
CREATE TABLE imdb_movies_1980s PARTITION OF imdb_movies
    FOR VALUES FROM (1980) TO (1990);

CREATE TABLE imdb_movies_1990s PARTITION OF imdb_movies
    FOR VALUES FROM (1990) TO (2000);

CREATE TABLE imdb_movies_2000s PARTITION OF imdb_movies
    FOR VALUES FROM (2000) TO (2010);

CREATE TABLE imdb_movies_2010s PARTITION OF imdb_movies
    FOR VALUES FROM (2010) TO (2020);
