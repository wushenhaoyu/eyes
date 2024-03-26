import { Upload } from "@/api/interface/index";
import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";
import { AxiosRequestConfig } from "axios";

/**
 * @name 文件上传模块
 */
// 图片上传
// 图片上传
export const registerHospital = (file: File, email: string, name: string, location: [string,string,string]) => {
  let formData = new FormData();
  formData.append('image', file);
  formData.append('email', email);
  formData.append('name', name);
  let locationStr = JSON.stringify(location);
  formData.append('location', locationStr);

  return http.upload(PORT1 + '/file/upload/img', formData, {}, { cancel: false });
};

// 视频上传
export const uploadVideo = (params: FormData) => {
  return http.post<Upload.ResFileUrl>(PORT1 + `/file/upload/video`, params, { cancel: false });
};
