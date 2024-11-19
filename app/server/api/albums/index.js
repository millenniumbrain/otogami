// server/api/music/albums.js
import Database from "better-sqlite3";

export default defineEventHandler((event) => {
  const db = new Database('./music_library.db');
  db.pragma('journal_mode = WAL');


  const sql = `
  SELECT Albums.Title AS albumTitle,
         Albums.AlbumID AS albumId,
         Artists.Name AS artistName,
         Artists.ArtistID AS artistId
  FROM Albums
  INNER JOIN Artists ON Albums.ArtistID = Artists.ArtistID
  ORDER BY Albums.Title
`;

const stmt = db.prepare(sql).all();

  // Group songs by album
  const groupedAlbums = stmt.reduce((acc, row) => {
    const { albumId, albumTitle, artistName, artistId } = row;

    if (!acc[albumId]) {
      acc[albumId] = {
        albumId,
        albumTitle,
        artistName,
        artistId
      };
    }
    return acc;
  }, {});

  // Convert object to array
  const result = Object.values(groupedAlbums);
  console.log(result)
  return result;
});