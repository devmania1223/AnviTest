import axios from "axios";
import { API_URL } from "../config/config";

const axiosInstance = axios.create({
    baseURL: API_URL,
    withCredentials: true,
  });

const verifyAuthentication = () => {
    // This method is used to verify authentication when user changes route manually.
    return axiosInstance.get(API_URL + "/dashboard/verify-authentication");
};
const getData = async () => {
    return axiosInstance.get(API_URL + "/dashboard/getData");
};
// eslint-disable-next-line import/no-anonymous-default-export
export default {
    verifyAuthentication,
    getData,
};