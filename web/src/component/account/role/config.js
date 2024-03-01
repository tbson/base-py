import { t } from 'ttag';
import RequestUtil from 'service/helper/request_util';

const urlMap = {
    base: {
        prefix: 'account/role',
        endpoints: {
            crud: ''
        }
    }
};
export const urls = RequestUtil.prefixMapValues(urlMap.base);

const headingTxt = t`Role`;
const name = headingTxt.toLowerCase();
export const messages = {
    heading: headingTxt,
    deleteOne: t`Do you want to remote this ${name}?`,
    deleteMultiple: t`Do you want to remote these ${name}?`
};

export const emptyRecord = {
    id: 0,
    title: '',
    profile_type: null,
    pem_ids: []
};

export const labels = {
    title: t`Role name`,
    profile_type: t`Profile type`,
    pem_ids: t`Permissions`
};
