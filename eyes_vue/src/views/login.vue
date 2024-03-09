<template>
<div :class=" bgControl?'bg_blur':''" class="bg" @click="start" style="background-color: white;width: 100vw;height: 100vh;background-image: url('../../public/img/bg.jpg');">
</div>
<div v-if="bgControl" :class=" mainControl?'main_show':'main_hide'" class="main" >
    <div style="text-align: center;color: white;font-size: 5vh;line-height: 15vh;">
        眼震诊疗平台
    </div>
    
</div>
</template>
  
  <style>
.bg{
    background-position: center center;
    /* 背景图不平铺 */
    background-repeat: no-repeat;
    /* 当内容高度大于图片高度时，背景图像的位置相对于viewport固定 */
    background-attachment: fixed;
    /* 让背景图基于容器大小伸缩 */
    background-size: cover;
    /* 设置背景颜色，背景图加载过程中会显示背景色 */
    background-color: #464646;
    
    transition: all 0.5s;
}
.bg_blur{
    filter: blur(4px);
}
.main{
    background-color: rgba(75, 81, 95, 0.3);
    box-shadow: 7px 7px 17px rgba(52, 56, 66, 0.8);
    border-radius: 20px;
    width:40vw;
    height:60vh;
    position: absolute;
    left: 50vw;
    top:50vh;
    transition: all 1s;
}
.main_hide{
    opacity: 0;
    transform: translate(-50%,-45%);
}
.main_show{
    opacity: 1;
    transform: translate(-50%,-50%);
}
</style>


<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  data() {
    return {
      bgControl:false,
      mainControl:false
    };
  },
  methods: {
    start()
    {
        this.bgControl = true
        console.log('start')
        setTimeout(()=>{
            this.mainControl = true
        },500)
    }
  }
});

</script>