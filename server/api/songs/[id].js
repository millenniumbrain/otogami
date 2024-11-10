import { defineEventHandler, getQuery, sendStream } from 'h3';
import Database from "better-sqlite3";
import fs from 'node:fs';

export default defineEventHandler(async (event) => {
  const db = new Database('./music_library.db');
  db.pragma('journal_mode = WAL');

  const id = event.context.params?.id;

  const songPath = db.prepare("SELECT FilePath as filePath FROM SongFiles WHERE SongID = ?").get(id);

  const { filePath } = songPath;

  console.log(filePath)
  if (!filePath || !fs.existsSync(filePath)) {
    throw createError({
      statusCode: 404,
      statusMessage: 'File not found'
    });
  }

  // Serve the file as a stream
  return sendStream(event, fs.createReadStream(filePath));
});