<!doctype html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title><?php echo $title ?></title>
        <link rel="stylesheet" type="text/css" href="/css/tuktuk.css">
        <link rel="stylesheet" type="text/css" href="/css/tuktuk.theme.css">
        <link rel="stylesheet" type="text/css" href="/css/tuktuk.icons.css">
        <link rel="stylesheet" type="text/css" href="/css/style.css">
        <script type="text/javascript" src="/js/functions.js"></script>
    </head>

    <body class="text thin" onload="setActiveLink('<?php if(isset($linkid)) echo $linkid; ?>')">
        <div id="wrapper">
            <div id="header" class="bck light padding">
                <div class="row">
                    <div class="column_6">
                        <a href="/"><img src="/img/logo.png" class="logo"/></a>
                    </div>
                    <div class="column_6  text right bold">
                        <a href="/signup">Signup</a>
                        <a href="/login" class="button small">Login</a>
                    </div>
                </div>
                </div>
                <section class="bck color">
  <div class="row text center">
    <nav data-tuktuk="menu" class="column_12 padding text bold">
      <a href="/post" id="pstlink">
        <span class="icon pencil"></span>Posts<small>(100)</small>
      </a>
      <a href="/categories" id="catlink">
        <span class="icon folder-open-alt"></span>Categories<small>(3)</small>
      </a>
      <a href="/administration" id="admlink">
          <span class="icon cog"></span>Administration
      </a>
      <a href="/about" id="abtlink">
          <span class="icon info-sign"></span>About
      </a>
    </nav>
  </div>
</section>
         