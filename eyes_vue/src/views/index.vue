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
      style="display: flex; justify-content: right;height: 6vh;"
    >
      <el-sub-menu index="2" style="font-size: 3vw;">
        <template #title>
      <el-avatar
        src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
      style="vertical-align: center;width: 4vh;height: 4vh;"/>  
      </template>
        <el-menu-item @click="clickMenu" style="height:3vh;font-size: 1vw;display: flex;justify-content: center;" index="info" >账号信息</el-menu-item>
        <el-menu-item @click="clickMenu" style="height:3vh;font-size: 1vw;display: flex;justify-content: center;" index="individual">个人中心</el-menu-item>
        <el-menu-item @click="clickMenu" style="height:3vh;font-size: 1vw;display: flex;justify-content: center;" index="setting">设置</el-menu-item>
      </el-sub-menu>
    </el-menu>
        </el-header>
        <!--此处结束header-->
        <el-container>
            <!--此处开始为aside-->
      <el-aside style="font-weight: 900;text-align: center;">
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
            <House style="width: 1em; height: 1em; margin-right: 8px;font-size: 1.5vw;" />
            <span>首页</span>
          </el-menu-item> 
          <el-menu-item  index="/patient1" @click="clickMenu">
            <User style="width: 1em; height: 1em; margin-right: 8px;font-size: 1.5vw;" />
            <span>待诊患者</span>
          </el-menu-item>
          <el-menu-item  index="/patient2" @click="clickMenu">
            <UserFilled style="width: 1em; height: 1em; margin-right: 8px;font-size: 1.5vw;" />
            <span>历史患者</span>
          </el-menu-item>
          
          <el-menu-item index="2" @click="clickMenu">
            <UserFilled style="width: 1em; height: 1em; margin-right: 8px;font-size: 1.5vw;" />
            <span>Two</span>
          </el-menu-item>
          <el-menu-item index="3" @click="clickMenu">   
            <Setting style="width: 1em; height: 1em; margin-right: 8px;font-size: 1.5vw;" />
            <span>Four</span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
      </el-aside>
      <!--此处结束aside-->
          <el-main style="background-color: white;">
            
            <RouterView></RouterView></el-main>
        </el-container>
      </el-container>
    </div>
  </template>

<style scoped>
:deep() .el-menu-item {
line-height:5vh;
font-size:2vw;
height:5vh;
}
:deep() .el-header {
  height: 6vh;
}
:deep() .el-aside {
  height: 94vh;
  width: 15vw;
}
:deep() .el-main {
  padding: 0;
  height: 94vh;
}


body{
    font-size:12px
}
span{
    font-size:1.5vw;
    font-weight:550
}
</style>

<script lang="ts">  
import { defineComponent } from 'vue';

export default defineComponent({
  data() {
    return {
      size:20
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
  


