import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://postgres:*******@localhost:5432/Music_Website')
connection = engine.connect()

print('Количество исполнителей в каждом жанре')
sel = connection.execute("""SELECT name, COUNT(performer_id) FROM genre g
                            JOIN genreperformer gp ON g.id = gp.genre_id 
                            GROUP BY g.name""").fetchall()
for i in sel:
    print(*i)
print('\nКоличество треков, вошедших в альбомы 2019-2020 годов')
sel = connection.execute("""SELECT COUNT(name) FROM track
                            WHERE album_id 
                            IN (SELECT id FROM album WHERE year BETWEEN 2019 and 2020)""").fetchall()
for i in sel:
    print(*i)
print('\nСредняя продолжительность треков по каждому альбому')
sel = connection.execute("""SELECT a.name, AVG(duration) FROM album a
                            JOIN track t ON a.id = t.album_id 
                            GROUP BY a.name""").fetchall()
for i in sel:
    print(*i)

print('\nВсе исполнители, которые не выпустили альбомы в 2020 году')
sel = connection.execute("""SELECT name FROM performer WHERE id
                            IN (SELECT performer_id FROM performeralbum WHERE album_id 
                            IN (SELECT id FROM album WHERE year <> 2020))""").fetchall()

for i in sel:
    print(*i)
print('\nНазвания сборников, в которых присутствует исполнитель Jax Jones')
sel = connection.execute("""SELECT name FROM collection WHERE id
                            IN (SELECT collection_id FROM collectiontrack WHERE track_id 
                            IN (SELECT id FROM track WHERE album_id 
                            IN (SELECT album_id FROM performeralbum WHERE performer_id 
                            IN (SELECT id FROM performer WHERE name = 'Jax Jones' ORDER BY id))))""").fetchall()
for i in sel:
    print(*i)
print('\nНазвание альбомов, в которых присутствуют исполнители более 1 жанра')
sel = connection.execute("""SELECT name FROM album a
                            JOIN performeralbum pa ON a.id = pa.album_id   
                            WHERE pa.performer_id IN
                            (SELECT p.id FROM performer p
                            JOIN genreperformer gp ON p.id = gp.performer_id 
                            GROUP BY p.id HAVING COUNT(genre_id) > 1)
                            """).fetchall()
for i in sel:
    print(*i)
print('\nНаименование треков, которые не входят в сборники')
sel = connection.execute("""SELECT name FROM track t
                            LEFT JOIN collectiontrack ct ON t.id = ct.track_id
                            WHERE ct.track_id IS NULL
                            """).fetchall()
for i in sel:
    print(*i)
print('\nИсполнителя(-ей), написавшего самый короткий по продолжительности трек')
sel = connection.execute("""SELECT name FROM performer p
                            JOIN performeralbum pa ON p.id = pa.performer_id 
                            WHERE pa.album_id IN
                            (SELECT a.id FROM album a
                            JOIN track t ON a.id = t.album_id
                            WHERE t.duration IN
                            (SELECT MIN(duration) FROM track))
                            """).fetchall()
for i in sel:
    print(*i)
print('\nНазвание альбомов, содержащих наименьшее количество треков')
sel = connection.execute("""SELECT a.name FROM album a
                            JOIN track t ON a.id = t.album_id
                            GROUP BY a.name HAVING COUNT(t.name) = 
                            (SELECT COUNT(t.name) FROM album a
                            JOIN track t ON a.id = t.album_id
                            GROUP BY a.name ORDER BY COUNT(t.name) LIMIT 1)
                            """).fetchall()
for i in sel:
    print(*i)


