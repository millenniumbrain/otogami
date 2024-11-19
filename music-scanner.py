import os
import sqlite3
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis

# Define supported audio file formats
SUPPORTED_FORMATS = {
    '.mp3': 'mp3',
    '.flac': 'flac',
    '.ogg': 'ogg'
}

# Reset and initialize the database
def reset_database(db_name="music_library.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Drop existing tables
    cursor.executescript('''
    DROP TABLE IF EXISTS PlaylistSongs;
    DROP TABLE IF EXISTS Playlists;
    DROP TABLE IF EXISTS SongFiles;
    DROP TABLE IF EXISTS Songs;
    DROP TABLE IF EXISTS Albums;
    DROP TABLE IF EXISTS Genres;
    DROP TABLE IF EXISTS Artists;
    ''')

    # Create tables
    cursor.executescript('''
    CREATE TABLE Artists (
        ArtistID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Bio TEXT,
        Country TEXT,
        FormedYear INTEGER
    );

    CREATE TABLE Genres (
        GenreID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL UNIQUE,
        Description TEXT
    );

    CREATE TABLE Albums (
        AlbumID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        ArtistID INTEGER,
        ReleaseYear INTEGER,
        CoverImageUrl TEXT,
        FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID) ON DELETE SET NULL
    );

    CREATE TABLE Songs (
        SongID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        ArtistID INTEGER,
        AlbumID INTEGER,
        GenreID INTEGER,
        Duration INTEGER NOT NULL,
        ReleaseDate TEXT,
        TrackNumber INTEGER,
        FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID) ON DELETE SET NULL,
        FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID) ON DELETE SET NULL,
        FOREIGN KEY (GenreID) REFERENCES Genres(GenreID) ON DELETE SET NULL
    );

    CREATE TABLE SongFiles (
        FileID INTEGER PRIMARY KEY AUTOINCREMENT,
        SongID INTEGER,
        FilePath TEXT NOT NULL,
        FileType TEXT NOT NULL,
        FileSize INTEGER,
        FOREIGN KEY (SongID) REFERENCES Songs(SongID) ON DELETE CASCADE
    );

    CREATE TABLE Playlists (
        PlaylistID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Description TEXT,
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE PlaylistSongs (
        PlaylistID INTEGER,
        SongID INTEGER,
        AddedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (PlaylistID, SongID),
        FOREIGN KEY (PlaylistID) REFERENCES Playlists(PlaylistID) ON DELETE CASCADE,
        FOREIGN KEY (SongID) REFERENCES Songs(SongID) ON DELETE CASCADE
    );
    ''')

    conn.commit()
    conn.close()
    print("Database has been reset.")

# Extract song metadata
def extract_metadata(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension not in SUPPORTED_FORMATS:
        return None

    audio = File(file_path)
    if audio is None:
        return None

    metadata = {
        "title": os.path.basename(file_path),
        "artist": "Unknown Artist",
        "duration": int(audio.info.length) if audio.info else 0,
        "file_type": SUPPORTED_FORMATS[file_extension],
        "file_size": os.path.getsize(file_path),
        "file_path": os.path.abspath(file_path).replace("\\", "/"),  # Convert to absolute path with forward slashes
        "track_number": None
    }

    # Extract metadata for specific formats
    if file_extension == ".mp3" and isinstance(audio, MP3):
        metadata["title"] = audio.get("TIT2", metadata["title"])
        metadata["artist"] = audio.get("TPE1", metadata["artist"])
        metadata["track_number"] = audio.get("TRCK", [""])[0].split("/")[0]
    elif file_extension == ".flac" and isinstance(audio, FLAC):
        metadata["title"] = audio.get("title", [metadata["title"]])[0]
        metadata["artist"] = audio.get("artist", [metadata["artist"]])[0]
        metadata["track_number"] = audio.get("tracknumber", [""])[0]
    elif file_extension == ".ogg" and isinstance(audio, OggVorbis):
        metadata["title"] = audio.get("title", [metadata["title"]])[0]
        metadata["artist"] = audio.get("artist", [metadata["artist"]])[0]
        metadata["track_number"] = audio.get("tracknumber", [""])[0]

    # Convert track number to integer if possible
    try:
        metadata["track_number"] = int(metadata["track_number"])
    except (ValueError, TypeError):
        metadata["track_number"] = None

    return metadata

def populate_database(directory_path, db_name="music_library.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Convert directory path to absolute path
    directory_path = os.path.abspath(directory_path)
    print(f"Scanning main directory: {directory_path}")

    # Loop only through immediate subdirectories
    for album_name in os.listdir(directory_path):
        album_path = os.path.join(directory_path, album_name)
        if os.path.isdir(album_path):  # Process only if it is a directory
            print(f"Scanning folder (album): {album_name}")

            # Process each file in the current album folder
            for file in os.listdir(album_path):
                file_path = os.path.join(album_path, file)

                # Only proceed if the file is a supported audio file
                if os.path.splitext(file)[1].lower() in SUPPORTED_FORMATS:
                    metadata = extract_metadata(file_path)

                    if metadata:
                        print(f"  Found file: {file}")
                        print(f"    - Artist: {metadata['artist']}")
                        print(f"    - Title: {metadata['title']}")
                        print(f"    - Duration: {metadata['duration']} seconds")
                        print(f"    - Track Number: {metadata['track_number']}")
                        print(f"    - File Type: {metadata['file_type']}")
                        print(f"    - File Size: {metadata['file_size']} bytes")
                        print(f"    - File Path: {metadata['file_path']}")

                        # Check if artist already exists
                        cursor.execute("SELECT ArtistID FROM Artists WHERE Name = ?", (metadata["artist"],))
                        artist_row = cursor.fetchone()
                        
                        if artist_row:
                            # Artist already exists, get their ID
                            artist_id = artist_row[0]
                        else:
                            # Insert new artist record
                            cursor.execute("INSERT INTO Artists (Name) VALUES (?)", (metadata["artist"],))
                            artist_id = cursor.lastrowid

                        # Check if album already exists for this artist
                        cursor.execute("SELECT AlbumID FROM Albums WHERE Title = ? AND ArtistID = ?", (album_name, artist_id))
                        album_row = cursor.fetchone()
                        
                        if album_row:
                            # Album already exists, get its ID
                            album_id = album_row[0]
                        else:
                            # Insert new album record
                            cursor.execute("INSERT INTO Albums (Title, ArtistID) VALUES (?, ?)", (album_name, artist_id))
                            album_id = cursor.lastrowid

                        # Insert song
                        cursor.execute('''
                        INSERT INTO Songs (Title, ArtistID, AlbumID, Duration, TrackNumber)
                        VALUES (?, ?, ?, ?, ?)
                        ''', (metadata["title"], artist_id, album_id, metadata["duration"], metadata["track_number"]))
                        song_id = cursor.lastrowid

                        # Insert song file details
                        cursor.execute('''
                        INSERT INTO SongFiles (SongID, FilePath, FileType, FileSize)
                        VALUES (?, ?, ?, ?)
                        ''', (song_id, metadata["file_path"], metadata["file_type"], metadata["file_size"]))

    conn.commit()
    conn.close()
    print("Database population complete.")

# Main execution
if __name__ == "__main__":
    music_directory = input("Enter the path to your main music directory: ")

    # Reset and populate the database
    reset_database()
    populate_database(music_directory)
    print("Database has been reset and populated successfully.")