<script>
import { $, jQuery } from 'jquery'
window.$ = $;
window.jQuery = jQuery;
// import '../assets/js/modernizr'
// import '../assets/js/cube.transitions'
// import '../assets/js/funny.text.min' // eslint-disable-line
import { funnyText } from '../assets/js/funny.text.min'

export default {
  name: 'about-page',
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
<div id="content">
  <div id="about-content">
    <div class="row">

      <div class="column_8">
        <span id="name-text">Misha Behersky</span>
        <table id="info-table" class="margin-top">
          <tbody>
            <tr>
              <td><i class="far fa-envelope fa-3x"></i></td>
              <td><span class="right"><a href="mailto:bmwant@gmail.com">bmwant@gmail.com</a></span></td>
            </tr>
            <tr>
              <td><i class="fab fa-skype fa-3x"></i></td>
              <td><span class="right"><a href="skype:most.wanted.21">most.wanted.21</a></span></td>
            </tr>
            <tr>
              <td><i class="fas fa-phone-volume fa-3x"></i></td>
              <td><span class="right"><a href="tel:+380986558186">0986558186</a></span></td>
            </tr>
            <tr>
              <td><i class="fab fa-facebook fa-3x"></i></td>
              <td><span class="right"><a href="https://www.facebook.com/misha.behersky" target="_blank">Facebook</a></span></td>
            </tr>
            <tr>
              <td><i class="fab fa-github fa-3x"></i></td>
              <td><span class="right"><a href="https://github.com/bmwant" target="_blank">github</a></span></td>
            </tr>
            <tr>
              <td><i class="fab fa-twitter fa-3x"></i></td>
              <td><span class="right"><a href="https://twitter.com/bmwant" target="_blank">twitter</a></span></td>
            </tr>
            <tr>
              <td><i class="fab fa-linkedin fa-3x"></i></td>
              <td><span class="right"><a href="https://www.linkedin.com/in/bmwant" target="_blank">LinkedIn</a></span></td>
            </tr>
            <tr>
              <td><i class="fab fa-stack-overflow fa-3x"></i></td>
              <td>
                <a href="https://stackoverflow.com/users/1744914/most-wanted" target="_blank">
                  <img src="https://stackoverflow.com/users/flair/1744914.png"
                       width="208" height="58" alt="profile for Most Wanted at Stack Overflow"
                       title="My profile at StackOverflow">
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="column_4">
        <div id="te-wrapper" class="te-wrapper">
          <div class="te-images">
            <img src="../assets/img/oneme.jpg"/>
            <img src="../assets/img/twome.jpg"/>
          </div>
          <div class="te-cover">
            <img src="../assets/img/oneme.jpg"/>
          </div>
          <div class="te-transition">
            <div class="te-cube-front te-cube-face te-front"></div>
            <div class="te-cube-left te-cube-face te-back"></div>
          </div>
        </div>
      </div>

    </div>
  </div>
</div>
</template>

<style>
@import '../assets/styles/cube-transition.css';
@import '../assets/styles/funny-text.css';
</style>
