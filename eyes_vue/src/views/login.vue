<template>
<div :class=" bgControl?'bg_blur':''" class="bg" @click="start" style="background-color: white;width: 100vw;height: 100vh;background-image: url('../../public/img/bg.jpg');">
</div>
<div v-if="bgControl" :class=" mainControl?'main_show':'main_hide'" class="main" style="display: flex;" >
    <!--<div style="text-align: center;color: white;font-size: 5vh;line-height: 15vh;">
        眼震诊疗平台
    </div>-->
    <span :class="isShowLogin1?'span_register_1':'span_register_2'" style="transition: all 1.5s;">
      <div v-if="!isShowLogin" class="color1" :class="isShowLogin1?'span_register_div_1':'span_register_div_2'" style="transition: all 0.5s;">
        <div style="height: 20vh;"></div>
        <div style="text-align: center;font-size: 3vw;height: 5vh;line-height: 5vh;font-weight: 600 ;">注册</div>
        <div style="height: 3vh;"></div>
        <div style="display: flex;justify-content: center;"><el-input class="border_color_1"
          v-model="userName"
          style="width: 60%;height: 5vh;"
          placeholder="邮箱"
          clearable
          :prefix-icon="Promotion"
          /></div>

          <div style="height: 2vh;"></div>

          <div style="display: flex;justify-content: center;"><el-input class="border_color_1"
          v-model="password"
          style="width: 60%;height: 5vh;"
          show-password= true
          placeholder="密码"
          type="password"
          clearable
          :prefix-icon="Lock"
          /></div>

          <div style="height: 2vh;"></div>

          <div style="display: flex;justify-content: center;"><el-input class="border_color_1"
          input-style="color: #2D51AD;"
          v-model="passwordConfirm"
          style="width: 60%;height: 5vh;"
          show-password= true
          placeholder="确认密码"
          type="password"
          clearable
          :prefix-icon="Lock"
          /></div>

          <div style="height: 2vh;"></div>

          <div style="display: flex;justify-content: center;"><el-input class="border_color_1"
          v-model="Id"
          style="width: 37.5%;height: 5vh;"
          placeholder="验证码"
          clearable
          :prefix-icon="Cellphone"/>
          <div style="width: 2.5%;"></div>
          <img src="../../public/img/bg.jpg" style="width: 20%;height: 5vh;border-radius: 5px;"/></div>


          <div style="height: 2vh;"></div>

          

          
          <div style="display: flex;justify-content: center;"><el-button @click="register" type="primary" style="width: 60%;height: 5vh;">注册</el-button></div>
          <div style="position: absolute;bottom: 1vh;width: 30vw;display: flex;justify-content: center;">  <el-link  @click.native="turn"  :underline="false" style="font-size: 1.2vw;">登录</el-link></div>
        </div>
    </span>
    <span :class="isShowLogin1?'span_login_1':'span_login_2'" style="transition: all 1.5s;">
      <div v-if="isShowLogin" class="color1" :class="isShowLogin1?'span_login_div_1':'span_login_div_2'" style="transition: all 0.5s;" >
        <div style="height: 20vh;"></div>
        <div style="text-align: center;font-size: 3vw;height: 5vh;line-height: 5vh;font-weight: 600 ;">登录</div>
        <div style="height: 3vh;"></div>
        <div style="display: flex;justify-content: center;"><el-input class="border_color_1"
          v-model="userName"
          style="width: 60%;height: 5vh;"
          placeholder="邮箱"
          clearable
          :prefix-icon="Promotion"
          /></div>

          <div style="height: 2vh;"></div>

          <div style="display: flex;justify-content: center;"><el-input class="border_color_1"
          v-model="password"
          style="width: 60%;height: 5vh;"
          placeholder="密码"
          show-password= true
          clearable
          type="password"
          :prefix-icon="Lock"
          /></div>

          <div style="height: 2vh;"></div>

          <div style="display: flex;justify-content: center;"><el-input class="border_color_1"
          v-model="Id"
          style="width: 37.5%;height: 5vh;"
          placeholder="验证码"
          clearable
          :prefix-icon="Cellphone"/>
          <div style="width: 2.5%;"></div>
          <img src="../../public/img/bg.jpg" style="width: 20%;height: 5vh;border-radius: 5px;"/></div>


          <div style="height: 2vh;"></div>

          
          <div style="display: flex;justify-content: center;"><el-button @click="enter" type="primary" style="width: 60%;height: 5vh;">登录</el-button></div>
          <div style="position: absolute;bottom: 1vh;width: 30vw;display: flex;justify-content: center;">  <el-link @click.native="turn" :underline="false" style="font-size: 1.2vw;">注册</el-link></div>
        </div>
    
    </span>
</div>
</template>
  
  <style>
  .span_register_div_1{
    opacity: 0;
  }
  .span_register_div_2{
    opacity: 1;
  }
  .span_login_div_1{
    opacity: 1;
  }
  .span_login_div_2
  {
    opacity: 0;
  }
  .border_color_1{
    border: #2D51AD 2px solid;
    border-radius: 5px;
  }
  .color1{
    color: #2D51AD;
  }
.span_login_1{
  display:inline-block;
  width: 30vw;height: 100%;
  background-color: aliceblue;
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
}
.span_login_2{
  width: 50vw;
  height: 100%;
  display:inline-block;
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
}
.span_register_1{
  width: 50vw;
  height: 100%;
  display:inline-block;
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
}
.span_register_2{
  display:inline-block;
  width: 30vw;height: 100%;
  background-color: aliceblue;
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
}
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
    background-position: center center;
    /* 背景图不平铺 */
    background-repeat: no-repeat;
    /* 当内容高度大于图片高度时，背景图像的位置相对于viewport固定 */
    background-attachment: fixed;
    /* 让背景图基于容器大小伸缩 */
    background-image:url('../../public/img/bg.jpg') ;
    background-size: cover;
    background-color: rgba(75, 81, 95, 0.3);
    box-shadow: 7px 7px 17px rgba(52, 56, 66, 0.8);
    border-radius: 20px;
    width:80vw;
    height:80vh;
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


<script  lang="ts">
import { ref } from 'vue'
import { Promotion,Lock,Cellphone } from '@element-plus/icons-vue'
export default defineComponent({
  data() {
    return {
      Cellphone:Cellphone,
      Promotion:Promotion,
      Lock:Lock,
      bgControl:false,
      mainControl:false,
      isShowLogin:true,
      isShowLogin1:true,
      userName:"",
      password:"",
      passwordConfirm:"",
      Id:""
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
    },
    enter()
    {
      if(this.userName == "" || this.password == "" || this.Id =="")
      {
        this.showError('登录信息填写不完整')
        return
      }
      else 
      {
        if(!this.checkEmail(this.userName))
        {
          this.showError('用户名格式错误')
          return
        }
        if(!this.checkPassword(this.password))
        {
          this.showError('用户名或密码有误')
          return
        }
        
      }
      this.showSuccess('登录成功')
      {
        setTimeout(()=>{
          this.$router.push('/index')
        },1000)
      }
    },
    turn(){
      this.isShowLogin1 = !this.isShowLogin1
      setTimeout(()=>{
        this.isShowLogin = !this.isShowLogin
        this.password = ""
        this.passwordConfirm =""
        this.userName = ""
        this.Id = ""
      },1500)
    },
    register()
    {
      if(this.userName == "" || this.password == "" || this.Id =="")
      {
        this.showError('注册信息填写不完整')
        return
      }
      else 
      {
        if(!this.checkEmail(this.userName))
        {
          this.showError('用户名格式错误')
          return
        }
        if(!this.checkPassword(this.password))
        {
          this.showError('密码格式有误')
          return
        }
        if(this.password != this.passwordConfirm)
        {
          console.log(this.password,this.passwordConfirm)
          this.showError('两次输入的密码不一致')
          return
        }
        let userName =  this.userName
        let password = this.password
        this.turn()
        this.showSuccess('注册成功')
        setTimeout(()=>{
          this.userName = userName
          this.password = this.password
        },1500)
    }
  },
    showError(e:string)
    {
      ElMessage.error(e)
    },
    showSuccess(e:string)
    {
      ElMessage({
        message: e,
        type: 'success',
      })
    }
    checkEmail(email)
    {
    // 使用正则表达式进行邮箱格式验证
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    console.log(regex.test(email))
    return regex.test(email);
    },
    checkPassword(password) {
    // 正则表达式用于检查密码是否包含至少一个大写字母、一个小写字母、一个数字和一个特殊符号
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    console.log(regex.test(password))
    return regex.test(password);
  },
  checkId(Id){//检查验证码是否正确

  }
  }
});

</script>