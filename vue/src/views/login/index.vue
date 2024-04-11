<template>
  <div class="login-container flx-center">
    <div class="login-box">
      <SwitchDark class="dark" />
      <div class="login-left">
        <img class="login-left-img" src="@/assets/images/bg.png" alt="login" />
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
  <p style="background:none;height: 5%;position: fixed;bottom: 0px;width: 100%;text-align: center;">     <a href="https://beian.miit.gov.cn/" target="_blank">陕ICP备2024028833号-1</a></p>
</template>

<script setup lang="ts" name="login">
import SwitchDark from "@/components/SwitchDark/index.vue";
import { RouterView } from "vue-router";
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
