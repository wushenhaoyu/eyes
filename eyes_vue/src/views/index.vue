<template>
    <div class="common-layout" id="index">
      <el-container>
        <!--此处开始为header-->
        <el-header style="padding: 0;">
            <el-menu
      class="el-menu-demo"
      mode="horizontal"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
      style="display: flex; justify-content: right;"
    >   
      <el-menu-item index="1">Processing Center</el-menu-item>
      <el-sub-menu index="2">
        <template #title>
      <el-avatar
        src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
      style="vertical-align: center;"/>
      </template>
        <el-menu-item index="2-1">item one</el-menu-item>
        <el-menu-item index="2-2">item two</el-menu-item>
        <el-menu-item index="2-3">item three</el-menu-item>
        <el-sub-menu index="2-4">
          <template #title>item four</template>
          <el-menu-item index="2-4-1">item one</el-menu-item>
          <el-menu-item index="2-4-2">item two</el-menu-item>
          <el-menu-item index="2-4-3">item three</el-menu-item>
        </el-sub-menu>
      </el-sub-menu>
    </el-menu>
        </el-header>
        <!--此处结束header-->
        <el-container>
            <!--此处开始为aside-->
      <el-aside style="width: 13vw;font-weight: 900;text-align: center;">
        <el-row class="tac">
      <el-col >
       <!-- <h5 class="mb-2">Custom colors</h5>-->
        <el-menu
          active-text-color="#ffd04b"
          background-color="#545c64"
          class="el-menu-vertical-demo"
          default-active="2"
          text-color="#fff"
        >
        <el-menu-item  index="/index" @click="clickMenu">
            <el-icon><icon-menu /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item  index="/patient1" @click="clickMenu">
            <el-icon><icon-menu /></el-icon>
            <span>待诊患者</span>
          </el-menu-item>
          <el-menu-item  index="/patient2" @click="clickMenu">
            <el-icon><icon-menu /></el-icon>
            <span>历史患者</span>
          </el-menu-item>
          <el-menu-item index="2" @click="clickMenu">
            <el-icon><icon-menu /></el-icon>
            <span>Navigator Two</span>
          </el-menu-item>
          <el-menu-item index="3" @click="clickMenu">   
            <el-icon><setting /></el-icon>
            <span>Navigator Four</span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
      </el-aside>
      <!--此处结束aside-->
          <el-main>
            
            <RouterView></RouterView></el-main>
        </el-container>
      </el-container>
    </div>
  </template>

<style>

/deep/ .el-menu-item {
    
}
</style>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  data() {
    return {
      greeting: 'Hello, Vue 3 with TypeScript!'
    };
  },
  methods: {
    clickMenu(e:any){
        console.log(e)
        this.$router.push(e.index)
    }
  }
});

</script>
  


