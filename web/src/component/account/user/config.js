import { t } from 'ttag';
import RequestUtil from 'service/helper/request_util';

const urlMap = {
    base: {
        prefix: 'account/user',
        endpoints: {
            crud: ''
        }
    },
    profile: {
        prefix: 'account',
        endpoints: {
            profile: 'profile'
        }
    }
};
export const urls = RequestUtil.prefixMapValues(urlMap.base);
export const profileUrls = RequestUtil.prefixMapValues(urlMap.profile);

const headingTxt = t`User`;
const name = headingTxt.toLowerCase();
export const messages = {
    heading: headingTxt,
    deleteOne: t`Do you want to remote this ${name}?`,
    deleteMultiple: t`Do you want to remote these ${name}?`
};

export const emptyRecord = {
    id: 0,
    last_name: '',
    first_name: '',
    email: '',
    mobile: '',
    password: '',
    is_active: true,
    role_ids: []
};

export const labels = {
    full_name: t`Fullname`,
    last_name: t`Lastname`,
    first_name: t`Firstname`,
    email: t`Email`,
    mobile: t`Phone number`,
    password: t`Password`,
    is_active: t`Active`,
    role_ids: t`Roles`
};
