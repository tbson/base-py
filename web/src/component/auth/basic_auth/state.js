import { atom } from 'recoil';

export const basicAuthUsernameSt = atom({
    key: 'basicAuthUsername',
    default: ''
});

export const basicAuthVerifyIdSt = atom({
    key: 'basicAuthVerifyId',
    default: ''
});

export const basicAuthVerifyCodeSt = atom({
    key: 'basicAuthVerifyCode',
    default: ''
});
