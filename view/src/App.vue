<script setup lang="ts">
import axios from 'axios'
import TitleColumn from './components/TitleColumn.vue'

const base = import.meta.env.BASE_URL

axios.interceptors.request.use((config: any) => {
  config.headers['cache-control'] = 'max-age=2147483647'; // always use cache, content never changes 
  config.url = base + config.url
  return config;
});

// parse charIndex (behind #)
const charIndex = window.location.hash.slice(1)

async function init() {
  // load levels
  const levels = await axios.get('/volume/levels', {responseType: 'text'})

  // setup columns

  // title column

  // text columns

  // svg column
}

</script>

<template>
  <div id=container>
    <TitleColumn />
    <TitleColumn />
    <TitleColumn />
    <TitleColumn />
  </div>
</template>

<style scoped>
#container {
  display: flex;
  overflow-x: scroll;
  height: 100vh;
}

.column {
  flex: 0 0 auto; /* set flex-grow, flex-shrink and flex-basis to 0, so the boxes don't stretch */
  width: 300px; /* set a fixed width for the boxes */
  margin-right: 10px; /* add margin between the boxes */
  height: 100vh;
  box-sizing: border-box;
  padding: 1rem; 
  overflow-y: scroll;
}

</style>
