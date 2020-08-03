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
        <a href="/post"><i class="fas fa-pencil-alt"></i>Posts</a>
        <a href="/categories"><i class="fas fa-search"></i>Find</a>
        <a href="/gallery"><i class="fas fa-camera-retro"></i>Photos</a>
        <!-- {% if user and user.is_admin() %} -->
        <a href="/ad"><i class="fas fa-cog"></i>Admin</a>
        <a href="/play"><i class="fas fa-flask"></i>Playground</a>
        <!-- {% endif %} -->
        <a href="/about"><i class="fas fa-chess-pawn"></i>About</a>
      </nav>
    </div>
  </section>
</div>
</template>
