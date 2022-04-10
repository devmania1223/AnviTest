import DashboardService from '../services/dashboard.service';

const checkAuth = async () => {
  try {
    await DashboardService.verifyAuthentication();
    return true;
  } catch {
    console.log("error")
    return false;
  }
};

export { checkAuth };
