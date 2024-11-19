const useMusicStore = defineStore('music', () => {
    // Define the song object
    const songs = ref([]);
    const isPlaying = ref(false);
    const currentTrack = ref(0);
    const currentAlbum = ref(0);

    // Action function to update the song data
    const updateSong = (newSongData) => {
        console.log("updating song")
        songs.value = newSongData;
    };

    const updatePlaying = (playing) => {
      isPlaying.value = playing;
    }

    const updateCurrentTrack = (currentTrack) => {
      debugger;
      currentTrack.value = currentTrack;
    }

    const updateCurrentAlbum = (albumId) => {
      currentAlbum.value = albumId;
    }

    return {
        updateSong,
        updatePlaying,
        updateCurrentTrack,
        updateCurrentAlbum,
        currentAlbum,
        isPlaying,
        currentTrack,
        songs
    };
});

export default useMusicStore;