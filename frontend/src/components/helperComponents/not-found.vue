<template>
  <div class="container">
    <div class="error-code">404</div>
    <div class="title">Page Not Found</div>
    <div class="description">
    The page you are looking for might have been removed,
    had its name changed, or is temporarily unavailable.
    </div>
    <a href="/" class="btn-home">Go Back Home</a>
  </div>

</template>>

<style scoped>


  .container {
    text-align: center;
    margin: auto;
    justify-content: center;
    display: flex;
    max-width: 500px;
    padding: 10%;
    flex-direction: column;
  }

  .error-code {
    font-size: 120px;
    font-weight: bold;
    background: black;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .title {
    font-size: 28px;
    margin-bottom: 15px;
  }

  .description {
    color: #808080;
    margin-bottom: 30px;
    line-height: 1.6;
  }

  .btn-home {
    display: inline-block;
    padding: 12px 25px;
    background: #000000;
    color: white;
    text-decoration: none;
    transition: 0.3s ease;
  }

  .btn-home:hover {
    background: #232323;
    transform: translateY(-2px);
  }

  @media (max-width: 600px) {
    .error-code {
      font-size: 80px;
    }
  }
</style>