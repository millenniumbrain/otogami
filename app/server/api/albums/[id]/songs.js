// server/api/music/albums.js
import Database from "better-sqlite3";

export default defineEventHandler((event) => {
  const db = new Database('./music_library.db');
  db.pragma('journal_mode = WAL');

  const id = event.context.params?.id;

  const sql = `
  SELECT 
    s.SongID AS songId,
    a.AlbumID AS albumId,
    s.Title AS songTitle,
    s.Duration AS songDuration,
    s.TrackNumber AS trackNumber 
  FROM Songs s
  INNER JOIN Albums a ON s.AlbumID = a.AlbumID
  INNER JOIN SongFiles sf ON s.SongID = sf.SongID
  WHERE a.albumID = ${id}
  ORDER BY s.SongID
`;

const stmt = db.prepare(sql).all();

  // Convert object to array
  return stmt;
});