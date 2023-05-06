<script setup lang=ts>
import config from '../config'

</script>

<template>
  <div class="column arrow">▶</div>
  <div class=column id=title-page>
    <h1> {{ config.title }} </h1>
    <h3> {{ config.subtitle }} </h3>
    <p> {{ config.description }} </p>
    <p>
      Dieser Text wurde mit dem Tool <i>recursive-gpt-summary</i> auf basis von ChatGPT zusammengefasst um ein leichtes und schnelles Erkunden zu ermöglichen. 
    </p>
    <p>
      Ihr können dieses Tool und auch diese WebApp selbst verwenden, es ist open source:
      <a href="https://github.com/felixniemeyer/recursive-gpt-summary" target="_blank">
        Recursive GPT Summary auf Github
      </a>
    </p>
  </div>
  <div class="column arrow">◀</div>
</template>

<style scoped>
#title-page {
  width: max(50vw, 50vh);
}
</style>
