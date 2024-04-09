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
  let params = {
    email,
    name,
    location: JSON.stringify(location),
  };
  console.log(file)
  return http.upload(PORT1 + '/hospital', file, params, {});
};

export const uploadImg = () => {
  // 实现上传图片的逻辑
};


// 视频上传
export const uploadVideo = (params: FormData) => {
  return http.post<Upload.ResFileUrl>(PORT1 + `/file/upload/video`, params, { cancel: false });
};


export const downloadVideo = (params: any )=> {
  return http.post(PORT1 + `/video/`, params, { loading: false });
}