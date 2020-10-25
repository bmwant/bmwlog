<script>
// import { imageBox } from '@/assets/js/imagebox'
import { collagePlus } from '@/assets/js/jquery.collagePlus.js'

export default {
  name: 'photos-page',
  data() {
    return {
      pageTitle: 'Instagram',
    }
  },
  mounted() {
    // imageBox()
  },
  methods: {
    onImgLoad() {
      // update gallery
      collagePlus('.gallery', {
        'effect': 'effect-2',
        'allowPartialLastRow': true,
        'targetHeight': 200,
        'direction': 'vertical'
      })
    }
  }
}
</script>

<template>
<div id="content">
  <div id="gallery-content">
    <div class="row">
      <div class="gallery">
        <a href="#">
          <img class="gallerimg" height="200" src="../assets/img/oneme.jpg" alt="Desc" @load="onImgLoad"/>
        </a>
         <a href="#">
          <img class="gallerimg" height="200" src="../assets/img/oneme.jpg" alt="Desc"/>
        </a>
        <a href="#">
          <img class="gallerimg" height="200" src="../assets/img/oneme.jpg" alt="Desc"/>
        </a>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>
@import '../assets/styles/gallery-transitions.css';
@import '../assets/styles/imagebox.css';
</style>
