<template>
  <div class="login-container flx-center">
    <div class="login-box">
      <SwitchDark class="dark" />
      <div class="login-left">
        <img class="login-left-img" src="@/assets/images/login_left.png" alt="login" />
      </div>
      <div class="login-form">
        <div class="login-logo">
          <img class="login-icon" src="@/assets/images/logo_eyes.png" alt="" />
          <h2 class="logo-text">眼震诊疗平台</h2>
        </div>
        <RouterView></RouterView>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="login">
import SwitchDark from "@/components/SwitchDark/index.vue";
import { RouterView } from "vue-router";
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
