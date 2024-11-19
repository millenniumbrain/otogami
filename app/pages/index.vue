<template>
<ul class="albums-list">
  <li v-for="(album, index) in data">
    <Album
    :id="album.albumId"
    :title="album.albumTitle"
    :artist-id="album.artistId"
    :artist="album.artistName"
    />
  </li>
</ul>

</template>
<script setup>
import Album from '~/components/Album.vue';
const { data } = useFetch('/api/albums');
</script>
<style lang="scss">
$gap: 20px;
$column-width: 12.5%;
.albums-list {
  display: flex;
  gap: $gap;
  padding: 10px;
  li {
    height: auto;
    list-style: none;
    flex: 0 0 calc($column-width - $gap);
    @media (max-width: 1440px) {
      flex: 0 0 calc(25% - $gap);
    }
  }
}
</style>