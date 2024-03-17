<template>
  <el-form ref="registerFormRef" :model="registerForm" :rules="loginRules" size="large">
    <el-form-item prop="username">
      <el-input v-model="registerForm.username" placeholder="输入邮箱" type="email">
        <template #prefix>
          <el-icon class="el-input__icon">
            <user />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="password">
      <el-input v-model="registerForm.password" type="password" placeholder="输入密码" show-password>
        <template #prefix>
          <el-icon class="el-input__icon">
            <lock />
          </el-icon>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item prop="authCode">
      <el-input v-model="registerForm.authCode" type="password" placeholder="输入医院认证码" show-password>
        <template #prefix>
          <el-icon class="el-input__icon">
            <lock />
          </el-icon>
        </template>
      </el-input>
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
    <el-button :icon="UserFilled" round size="large" type="primary" :loading="loading" @click="register"> 注册 </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Register } from "@/api/interface";
import { CircleClose, UserFilled } from "@element-plus/icons-vue";
import { LOGIN } from "@/config";
import type { ElForm } from "element-plus";
import { registerApi } from "@/api/modules/login";

const router = useRouter();

type FormInstance = InstanceType<typeof ElForm>;
const registerFormRef = ref<FormInstance>();
const loginRules = reactive({
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
  authCode: [{ required: true, message: "请输入医院认证码", trigger: "blur" }],
  verificationCode: [{ required: true, message: "请输入邮箱验证码", trigger: "blur" }]
});

const loading = ref(false);
const registerForm = reactive<Register.ReqRegisterForm>({
  username: "",
  password: "",
  authCode: "",
  verificationCode: ""
});

// login
const register = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate(async valid => {
    if (!valid) return;
    loading.value = true;
    try {
      // 1.执行登录接口
      const { data } = await registerApi({ ...registerForm, password: md5(registerForm.password) });

      console.log(data);
      // 4.跳转到首页
      router.push(LOGIN);
      ElNotification({
        title: getTimeState(),
        message: "注册成功！",
        type: "success",
        duration: 3000
      });
    } finally {
      loading.value = false;
    }
  });
};

const login = () => {
  router.push("login");
};

const getVer = () => {
  console.log("获取验证码");
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
</style>
