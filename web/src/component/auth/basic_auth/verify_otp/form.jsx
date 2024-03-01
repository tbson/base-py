import * as React from 'react';
import { useRef, useEffect } from 'react';
import { t } from 'ttag';
import { useSetRecoilState, useRecoilValue } from 'recoil';
import { Form, Input } from 'antd';
import FormUtil from 'service/helper/form_util';

import { otpUrls } from '../config';
import {
    basicAuthUsernameSt,
    basicAuthVerifyIdSt,
    basicAuthVerifyCodeSt
} from '../state';

const formName = 'VerifyOtpForm';

/**
 * VerifyOtpForm.
 *
 * @param {Object} props
 * @param {string} props.verify_id
 * @param {string} props.username
 * @param {onChange} onChange
 * @returns {ReactElement}
 */
export default function VerifyOtpForm({ form, onChange }) {
    const inputRef = useRef(null);
    const username = useRecoilValue(basicAuthUsernameSt);
    const verifyId = useRecoilValue(basicAuthVerifyIdSt);
    const setBasicAuthVerifyCode = useSetRecoilState(basicAuthVerifyCodeSt);

    useEffect(() => {
        inputRef.current.focus({ cursor: 'end' });
    }, []);

    const initialValues = { verify_code: '' };

    const formAttrs = {
        verify_code: {
            name: 'verify_code',
            label: t`OTP code`,
            rules: [FormUtil.ruleRequired()]
        }
    };
    return (
        <Form
            form={form}
            name={formName}
            labelCol={{ span: 6 }}
            wrapperCol={{ span: 18 }}
            initialValues={{ ...initialValues }}
            onFinish={(payload) => {
                setBasicAuthVerifyCode(payload.verify_code);
                FormUtil.submit(otpUrls.checkOtp, { ...payload, verify_id: verifyId })
                    .then(() => onChange(payload.verify_code))
                    .catch(FormUtil.setFormErrors(form));
            }}
        >
            <p>
                {t`OTP code has been sent to`}: {username}
            </p>
            <Form.Item {...formAttrs.verify_code}>
                <Input ref={inputRef} />
            </Form.Item>
        </Form>
    );
}

VerifyOtpForm.displayName = formName;
VerifyOtpForm.formName = formName;
