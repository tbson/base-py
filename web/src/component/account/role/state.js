import { atom } from 'recoil';

export const roleOptionSt = atom({
    key: 'roleOption',
    default: {
        pem: [],
        profile_type: []
    }
});
