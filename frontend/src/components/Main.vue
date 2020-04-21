<template>
  <div id="app">
    <div class="wrapper">
      <b-navbar toggleable="lg" type="dark" variant="primary">
        <b-container>
          <b-navbar-brand :to="{ name: 'Root'}">
            <img
              src="../images/ionos-logo.png"
              class="d-inline-block align-top brand-logo"
              alt="IONOS Logo"
            />
            Test Executor
          </b-navbar-brand>
        </b-container>
      </b-navbar>
      <main role="main" class="container pt-3">
        <transition name="fade" mode="out-in">
          <router-view :key="$route.fullPath"></router-view>
        </transition>
      </main>
      <footer class="footer">
        <div class="container">
          <small class="my-0 text-muted">
            &copy;
            <a class="text-muted" href="https://janw.xyz">Jan Willhaus</a>
            2020. Licensed under Apache License 2.0.
          </small>
        </div>
      </footer>
    </div>
  </div>
</template>


<style>
.brand-logo {
  max-height: 30px;
}

.fade-enter-active,
.fade-leave-active {
  transition-duration: 0.1s;
  transition-property: opacity;
  transition-timing-function: ease-in-out;
}

.fade-enter,
.fade-leave-active {
  opacity: 0;
}
</style>

<script>
import { BNavbar, BNavbarBrand } from "bootstrap-vue";
export default {
  components: {
    BNavbar,
    BNavbarBrand
  }
};
</script>
