<template>
<ul>
</ul>
<ul>
  <li v-for="(album, index) in data">
    <ul>
      <li v-for="(song, index) in album.songs">{{ song.songTitle }} | {{ album.albumTitle }} | {{duration(song.songDuration)}}</li>
    </ul>
  </li>
</ul>
  <audio controls>
  <source :src="music" type="audio/ogg">
  Your browser does not support the audio element.
</audio>

</template>
<script setup>
const music  = '/api/songs/2'
const { data } = useFetch('/api/albums');

function duration(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  return `${minutes}:${seconds}`;
}

</script>