<script>
export default {
  name: 'banners-block',
  methods: {
  },
  mounted() {
  }
}
</script>

<template>
<div class="column_4 hide-tablet hide-phone">
  <div class="padding margin banner-block">
    <div class="myrow">Paid ads</div>
    <div class="myrow">
      <a href="#" target="_blank">
        <img width="300" src="@/assets/banner01.png" alt="Alt text" title="this is title"/>
      </a>
    </div>
  </div>

  <div class="padding margin">
    <a href="https://internetdefenseleague.org" target="_blank">
      <img width="300"
            src="https://internetdefenseleague.org/images/badges/final/super_badge.png"
            alt="Member of The Internet Defense League"/>
    </a>
  </div>

  <div class="padding margin">
    <div class="quote-text">
      Some quote text here
    </div>
    <div class="quote-author">
      Some quote author here
    </div>
  </div>
</div>
</template>

<style>

</style>
