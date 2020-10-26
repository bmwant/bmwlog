<template>
<div>
  <div id="header" class="bck light padding">
    <div class="row">
      <div class="column_6">
          <a href="/"><img src="../assets/logo.png" class="logo"/></a>
      </div>
      <div class="column_6 text right bold hide-phone">
      <!-- {% set user = app.current_user %} -->
      <!-- {% if user %} -->
          Hey, <a href="/account">username</a>
          <a href="/logout" class="button small secondary">Logout</a>
      <!-- {% else %} -->
          <a href="/signup">Sign up</a>
          <a href="/login" class="button small">Login</a>
      <!-- {% endif %} -->
      </div>
    </div>
  </div>

  <section id="site-joke" class="bck color">
    <div class="row text center bold">
      <div class="column_12 padding text bold" id="joke-text">
        this is site joke
      </div>
    </div>
  </section>

  <section id="site-menu" class="bck color">
    <div class="row text center">
      <nav data-tuktuk="menu" class="column_12 padding text bold">
        <router-link to="/post"><i class="fas fa-pencil-alt"></i>Posts</router-link>
        <router-link to="/search"><i class="fas fa-search"></i>Find</router-link>
        <router-link to="/gallery"><i class="fas fa-camera-retro"></i>Photos</router-link>
        <!-- {% if user and user.is_admin() %} -->
        <router-link to="/ad"><i class="fas fa-cog"></i>Admin</router-link>
        <router-link to="/play"><i class="fas fa-flask"></i>Playground</router-link>
        <!-- {% endif %} -->
        <router-link to="/about"><i class="fas fa-chess-pawn"></i>About</router-link>
      </nav>
    </div>
  </section>
</div>
</template>
