<template>
  <div>
    <ul>
      <li v-for="(song, index) in songs">{{ song.songTitle }}</li>
    </ul>
  </div>
</template>
<script setup>
const route = useRoute();
const id = route.params.id;

const { data: songs } = await useFetch(`/api/albums/${id}/songs`);

console.log(songs.value)
</script>