<script setup lang=ts>
import config from '../config'

</script>

<template>
  <div class=column>
    <h1> {{ config.title }} </h1>
    <h3> {{ config.subtitle }} </h3>
    <p> {{ config.description }} </p>
    <p> {{ config.description }} </p>
    <p>
      Dieser Text wurde mit dem Tool <i>recursive-gpt-summary</i> auf basis von ChatGPT zusammengefasst um ein leichtes und schnelles Erkunden zu ermöglichen. 
    </p>
    <p>
      Ihr können dieses Tool und auch diese WebApp selbst verwenden, es ist Open Source:
      <a href="https://github.com/felixniemeyer/recursive-gpt-summary" target="_blank">
        Recursive GPT Summary auf Github
      </a>
    </p>
  </div>
</template>

<style scoped>
</style>
