<template>
<ul>
  <li v-for="(album, index) in data">
    {{ album.albumTitle }}
  </li>
</ul>

</template>
<script setup>
const { data } = useFetch('/api/albums');
</script>