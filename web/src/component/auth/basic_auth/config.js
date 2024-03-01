import { t } from 'ttag';
import RequestUtil from 'service/helper/request_util';

const urlMap = {
    base: {
        prefix: 'auth/basic-auth',
        endpoints: {
            login: 'login',
            resetPwd: 'reset-pwd',
            changePwd: 'change-pwd'
        }
    },
    profile: {
        prefix: 'account',
        endpoints: {
            profile: 'profile'
        }
    },
    otp: {
        prefix: 'verify/otp',
        endpoints: {
            sendResetPwdOtp: 'send-reset-pwd-otp',
            resendOtp: 'resend-otp',
            checkOtp: 'check-otp'
        }
    }
};

export const urls = RequestUtil.prefixMapValues(urlMap.base);
export const otpUrls = RequestUtil.prefixMapValues(urlMap.otp);

const headingTxt = t`Profile`;
export const messages = {
    heading: headingTxt
};
