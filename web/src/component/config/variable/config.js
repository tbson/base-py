import { t } from 'ttag';
import RequestUtil from 'service/helper/request_util';

const urlMap = {
    base: {
        prefix: 'config/variable',
        endpoints: {
            crud: ''
        }
    }
};
export const urls = RequestUtil.prefixMapValues(urlMap.base);

const headingTxt = t`Variable`;
const name = headingTxt.toLowerCase();
export const messages = {
    heading: headingTxt,
    deleteOne: t`Do you want to remote this ${name}?`,
    deleteMultiple: t`Do you want to remote these ${name}?`
};

export const labels = {
    uid: t`UID`,
    value: t`Value`,
    description: t`Description`,
    type: t`Type`
};
