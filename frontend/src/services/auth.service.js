import axios from "axios";
import { API_URL } from "../config/config";
const axiosInstance = axios.create({
    baseURL: API_URL,
    withCredentials: true,
  });
const register = async (email, password, passwordRepeat) => {
    await axiosInstance
        .post(API_URL + "/auth/register", {
            email, password, passwordRepeat
        });
    console.log(email, password);
};
const login = async (email, password) => {
    await axiosInstance
        .post(API_URL + "/auth/login", {
            email, password,
        });
    console.log(email, password);
};
const logout = async () => {
    return axiosInstance.post(API_URL + "/auth/logout");
};
// eslint-disable-next-line import/no-anonymous-default-export
export default {
    register,
    login,
    logout,
};