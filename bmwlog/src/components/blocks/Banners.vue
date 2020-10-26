<script>
// import '../assets/js/modernizr'
// import '../assets/js/cube.transitions'
// import '../assets/js/funny.text.min' // eslint-disable-line

export default {
  name: 'banners-block',
  data() {
    return {
      pageTitle: 'Get in touch',
    }
  },
  methods: {
  },
  mounted() {
    funnyText('#name-text', {
      speed: 700,
      borderColor: 'black',
      activeColor: 'white',
      color: 'black',
      fontSize: '5em',
      direction: 'both'
    });
  }
}
</script>

<template>
    <div class="column_4 hide-tablet hide-phone">
      <div class="padding margin banner-block">
        {% if banner %}
        <div class="myrow">Paid ads</div>
        <div class="myrow">
          <a href="{{ banner.link }}" {% if banner.link != "#" %}target="_blank"{% endif %}>
          <img width="300" src="/img/banners/{{ banner.img }}" alt="{{ banner.desc }}" title="{{ banner.desc }}"/></a>
        </div>
        {% endif %}
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
          {{ quote.text }}
        </div>
        <div class="quote-author">
          {{ quote.author }}
        </div>
      </div>
    </div>
</template>

<style>
@import '../assets/styles/cube-transition.css';
</style>
