<template>
  <el-form ref="registerFormRef" :model="registerForm" :rules="loginRules" size="large">
    <el-form-item prop="email">
      <el-input v-model="registerForm.email" placeholder="输入医院绑定邮箱" type="email">
        <template #prefix>
          <el-icon class="el-input__icon">
            <user />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="name">
      <el-input v-model="registerForm.name" placeholder="输入医院名称" type="email">
        <template #prefix>
          <el-icon class="el-input__icon">
            <user />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item >
    <UploadImgs v-model:file-list="registerForm.photo" :limit="3" height="90px" width="90px" border-radius="50%">
              <template #empty>
                <el-icon><Picture /></el-icon>
                <span>医院资质证明</span>
              </template>
            </UploadImgs>
          </el-form-item>
          <el-form-item prop="location">          
              <el-cascader
              style="width: 100%;"
            size="large"
            :options="pcaTextArr"
            v-model="registerForm.location">
          </el-cascader>
  </el-form-item>
    <el-form-item prop="verificationCode">
      <el-input
        style="width: 55%; margin-right: 5%"
        v-model="registerForm.verificationCode"
        maxlength="5"
        placeholder="输入验证码"
      >
        <template #prefix>
          <el-icon class="el-input__icon">
            <lock />
          </el-icon>
        </template>
      </el-input>
      <el-button :icon="CircleClose" @click="getVer" style="width: 40%"> 获取验证码 </el-button>
    </el-form-item>
  </el-form>
  <div class="login-btn">
    <el-button :icon="CircleClose" round size="large" @click="login"> 登录 </el-button>
    <el-button :icon="UserFilled" round size="large" type="primary" :loading="loading" @click="registerhospital(registerFormRef)">
      注册
    </el-button>
  </div>
  <div style="display: flex;justify-content: end;"><el-link type="primary" @click="register">注册医生？</el-link></div>
</template>

<script setup lang="ts">
import {
  provinceAndCityData,
  pcTextArr,
  regionData,
  pcaTextArr,
  codeToText,
} from "element-china-area-data";
import UploadImgs from "@/components/Upload/Imgs.vue";
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Register } from "@/api/interface";
import { CircleClose, UserFilled } from "@element-plus/icons-vue";
import { ElNotification, type ElForm } from "element-plus";
import { emailApi, registerApi } from "@/api/modules/login";
import { getTimeState } from "@/utils";
import md5 from "md5";


const options = regionData;
      
const router = useRouter();

/*const fromModel = ref({
  avatar: "",
  photo: [{ name: "img", url: "https://i.imgtg.com/2023/01/16/QR57a.jpg" }],
  username: "",
  idCard: "",
  email: ""
});*/


type FormInstance = InstanceType<typeof ElForm>;
const registerFormRef = ref<FormInstance>();
const loginRules = reactive({
  email: [{ required: true, message: "请输入医院绑定邮箱", trigger: "blur" }],
  name: [{ required: true, message: "请输入医院名称", trigger: "blur" }],
  verificationCode: [{ required: true, message: "请输入邮箱验证码", trigger: "blur" }],
  photo:[{ required: true, message: "上传医院资质证明", trigger: "blur" }],
  location:[{ required: true, message: "选择医院所在地区", trigger: "blur" }]
});

const loading = ref(false);
const registerForm = reactive<Register.ReqRegisterHospitalForm>({
  email: "",
  name:"",
  verificationCode: "",
  photo:[{name:'',url:''}],
  location:["","",""]
});

const register = () =>{
  console.log(registerForm)
  router.push("/login/register");
}

// login
const registerhospital = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate(async valid => {
    if (!valid) return;
    loading.value = true;
    try {
      // 1.执行登录接口
      //const data = await registerApi({ ...registerForm, password: md5(registerForm.password) });
      console.log(data);
      // 4.跳转到首页
      ElNotification({
        title: getTimeState(),
        message: "注册成功！",
        type: "success",
        duration: 3000
      });
    } finally {
      loading.value = false;
      router.push("login");
    }
  });
};

const login = () => {
  router.push("login");
};

const getVer = () => {
  let email = registerForm.email;
  emailApi({ email: email });
};
// resetForm
/*const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();
};*/

onMounted(() => {
  // 监听 enter 事件（调用登录）
  document.onkeydown = (e: KeyboardEvent) => {
    e = (window.event as KeyboardEvent) || e;
    if (e.code === "Enter" || e.code === "enter" || e.code === "NumpadEnter") {
      if (loading.value) return;
      //login(registerFormRef.value);
    }
  };
});
</script>

<style scoped lang="scss">
@import "../index.scss";
.el-form-item {
  display: flex;
  justify-content: center;
      }
</style>
