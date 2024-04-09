<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" size="80vw" :title="`${drawerProps.title}用户`">
    <div style="display: flex;">
    <div style="width: 30vw">
      <el-form
        ref="ruleFormRef"
        label-width="100px"
        label-suffix=" :"
        :rules="rules"
        :disabled="drawerProps.isView"
        :model="drawerProps.row"
        :hide-required-asterisk="drawerProps.isView"
      >
        <el-form-item label="用户姓名" prop="username">
          <el-input  v-model="drawerProps.row!.username" placeholder="请填写用户姓名" clearable></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select v-model="drawerProps.row!.gender" placeholder="请选择性别" clearable>
            <el-option v-for="item in genderType" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="身份证号" prop="idCard">
          <el-input v-model="drawerProps.row!.idCard" placeholder="请填写身份证号" clearable></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="email">
          <el-input v-model="drawerProps.row!.email" placeholder="请填写手机号" clearable></el-input>
        </el-form-item>
        <el-form-item label="居住地址" prop="address">
          <el-input v-model="drawerProps.row!.address" placeholder="请填写居住地址" clearable></el-input>
        </el-form-item>
        <el-form-item label="患者描述" prop="address">
          <el-input v-model="drawerProps.row!.address" placeholder="请填写居住地址" clearable></el-input>
        </el-form-item>
      </el-form>
    </div>
    <div style="display: flex;justify-content: center;width: 50vw;">
      <video-player
      style="width: 90%;height: 100%;"
    :src="VideoUrl"
    poster=""
    :controls="true"
    :autoplay="true"
    :loop="true"
    :volume="0.6"
  />
    </div>
  </div>
    <div>
      <div style="height: 1vh;"></div>
      <el-form
        label-width="100px"
        label-suffix=" :"
        :rules="rules"
        :model="drawerProps.row"
        :hide-required-asterisk="drawerProps.isView"
      >
      <el-form-item label="眼震视图">
      <img style="height: 37.5vw;width:100%;" :src="ImageUrl">
  </el-form-item>
  <el-form-item label="机器判断">
   判断为右跳型眼震
    </el-form-item>
      <el-form-item label="医生评价">
          <el-input
    v-model="textarea1"
    style="width: 100vw;margin-bottom: 20px;"
    :rows="5"
    type="textarea"
    placeholder="Please input"
  />
        </el-form-item>
    </el-form></div>
    
    <ProTable
      ref="proTable"
      :columns="columns"
      :request-api="getTableList"
      :init-param="initParam"
      :data-callback="dataCallback"
      @darg-sort="sortTable"
    >
    <template #operation="scope">
        <el-button type="primary" link :icon="View" @click="openDrawer('查看', scope.row)">查看</el-button>
      </template>
    </ProTable>
    <UserDrawer1 ref="drawerRef" />

    <template #footer>
      <el-button @click="drawerVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSubmit">提交</el-button>
    </template>
  </el-drawer>
</template>

<script setup lang="ts"  name="UserDrawer">
import { ref, reactive ,onMounted  } from "vue";
import { genderType } from "@/utils/dict";
import { ElMessage, FormInstance,ElMessageBox, ElNotification  } from "element-plus";
import { User } from "@/api/interface";
import { useRouter } from "vue-router";
import { useHandleData } from "@/hooks/useHandleData";
import { useDownload } from "@/hooks/useDownload";
/*import { useAuthButtons } from "@/hooks/useAuthButtons";*/
import ProTable from "@/components/ProTable/index.vue";
import ImportExcel from "@/components/ImportExcel/index.vue";
import UserDrawer1 from "@/views/proTable/components/UserDrawer1.vue";
import { ProTableInstance, ColumnProps, HeaderRenderScope } from "@/components/ProTable/interface";
import { CirclePlus, Delete, Download, Upload, View } from "@element-plus/icons-vue";
import {
  getUserList,
  deleteUser,
  editUser,
  addUser,
  advice,
  //changeUserStatus,
  //resetUserPassWord,
  exportUserInfo,
  BatchAddUser,
  // getUserStatus,
  getUserGender,
getPatientHistroyList
} from "@/api/modules/user";
import { VideoPlayer } from '@videojs-player/vue'
import 'video.js/dist/video-js.css'
import { downloadVideo } from "@/api/modules/upload";
//import UploadImg from "@/components/Upload/Img.vue";
//import UploadImgs from "@/components/Upload/Imgs.vue";


const textarea1 = ref('')

const rules = reactive({
  avatar: [{ required: true, message: "请上传用户头像" }],
  photo: [{ required: true, message: "请上传用户照片" }],
  username: [{ required: true, message: "请填写用户姓名" }],
  gender: [{ required: true, message: "请选择性别" }],
  idCard: [{ required: true, message: "请填写身份证号" }],
  email: [{ required: true, message: "请填写手机号" }],
  address: [{ required: true, message: "请填写居住地址" }]
});

interface DrawerProps {
  title: string;
  isView: boolean;
  row: Partial<User.ResUserList>;
  api?: (params: any) => Promise<any>;
  getTableList?: () => void;
  id:string
}

const drawerVisible = ref(false);
const drawerProps = ref<DrawerProps>({
  isView: false,
  title: "",
  row: {},
  id:""
});

let VideoUrl = ref("");
let ImageUrl = ref("");
// 接收父组件传过来的参数
const acceptParams = async (params: DrawerProps) => {
  if (drawerProps.value.id != params.id) {
    drawerProps.value = params;
    const data =  await downloadVideo({id:drawerProps.value.id})
    console.log(data)
    VideoUrl = data.video
    ImageUrl = data.picture
  }    
  drawerVisible.value = true;
};

// 提交数据（新增/编辑）
const ruleFormRef = ref<FormInstance>();
const handleSubmit = async (params: any) => {
  console.log(textarea1.value)
  let completeParams = {...drawerProps.value.row,advice:textarea1.value};
  let data = await advice(completeParams);
  if(data.success)
  {
    drawerVisible.value = false
    ElNotification({
        title: 'success',
        message: "诊疗成功！",
        type: "success",
        duration: 3000
      });
  }
};

defineExpose({
  acceptParams
});
const dataCallback = (data: any) => {
  return {
    list: data.list,
    total: data.total,
    pageNum: data.pageNum,
    pageSize: data.pageSize
  };
};

const getTableList = (params: any) => {
  
  let newParams = JSON.parse(JSON.stringify(params));
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;

  // Assuming drawerProps.value.row is also an object
  let completeParams = {...newParams, ...drawerProps.value.row};

  return getPatientHistroyList(completeParams);
};

const router = useRouter();
const showDeleteButton = false;

// 跳转详情页
const toDetail = () => {
  router.push(`/proTable/patientCurrent/detail/${Math.random().toFixed(3)}?params=detail-page`);
};
const initParam = reactive({ type: 1 });
// ProTable 实例
const proTable = ref<ProTableInstance>();

// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  { type: "sort", label: "Sort", width: 80 },
  { type: "expand", label: "Expand", width: 85 },
  { prop: "username", label: "用户姓名", width: 85 },
  {
    prop: "gender",
    label: "性别",
  },
  /* {
    prop: "status",
    label: "用户状态",
    enum: getUserStatus,
    search: { el: "tree-select", props: { filterable: true } },
    fieldNames: { label: "userLabel", value: "userStatus" },
    render: scope => {
      return (
        <>
          {BUTTONS.value.status ? (
            <el-switch
              model-value={scope.row.status}
              active-text={scope.row.status ? "启用" : "禁用"}
              active-value={1}
              inactive-value={0}
              onClick={() => changeStatus(scope.row)}
            />
          ) : (
            <el-tag type={scope.row.status ? "success" : "danger"}>{scope.row.status ? "启用" : "禁用"}</el-tag>
          )}
        </>
      );
    }
  },*/
  {
    prop: "user.detail.age",
    label: "年龄"
  },
  { prop: "idCard", label: "身份证号" },
  { prop: "email", label: "手机号" },
  { prop: "address", label: "居住地址" },
  /*{
    prop: "status",
    label: "用户状态",
    enum: getUserStatus,
    search: { el: "tree-select", props: { filterable: true } },
    fieldNames: { label: "userLabel", value: "userStatus" },
    render: scope => {
      return (
        <>
          {BUTTONS.value.status ? (
            <el-switch
              model-value={scope.row.status}
              active-text={scope.row.status ? "启用" : "禁用"}
              active-value={1}
              inactive-value={0}
              onClick={() => changeStatus(scope.row)}
            />
          ) : (
            <el-tag type={scope.row.status ? "success" : "danger"}>{scope.row.status ? "启用" : "禁用"}</el-tag>
          )}
        </>
      );
    }
  },*/
  {
    prop: "createTime",
    label: "挂号时间",
    width: 180,
    search: {
      el: "date-picker",
      span: 2,
      props: { type: "datetimerange", valueFormat: "YYYY-MM-DD HH:mm:ss" },
      defaultValue: ["2022-11-12 11:35:00", "2024-12-12 11:35:00"]
    }
  },
  { prop: "operation", label: "操作", fixed: "right", width: 120 }
]);

const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};

const drawerRef = ref<InstanceType<typeof UserDrawer1> | null>(null);
const openDrawer = (title: string, row: Partial<User.ResUserList> = {}) => {
  const params = {
    title,
    isView: title === "查看",
    row: { ...row },
    api: title === "新增" ? addUser : title === "编辑" ? editUser : undefined,
    getTableList: proTable.value?.getTableList
  };
  drawerRef.value?.acceptParams(params);
};
</script>
