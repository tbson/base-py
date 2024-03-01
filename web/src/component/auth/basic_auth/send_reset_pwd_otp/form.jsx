import * as React from 'react';
import { useRef, useEffect } from 'react';
import { t } from 'ttag';
import { useSetRecoilState } from 'recoil';
import { Form, Input } from 'antd';
import FormUtil from 'service/helper/form_util';
import { otpUrls } from '../config';
import { basicAuthUsernameSt, basicAuthVerifyIdSt } from '../state';

const formName = 'SendResetPwdOtpForm';

/**
 * SendResetPwdOtpForm.
 *
 * @param {Object} object
 * @param {FormCallback} object.onChange
 */
export default function SendResetPwdOtpForm({ onChange }) {
    const inputRef = useRef(null);
    const [form] = Form.useForm();
    const setBasicAuthUsername = useSetRecoilState(basicAuthUsernameSt);
    const setBasicAuthVerifId = useSetRecoilState(basicAuthVerifyIdSt);

    useEffect(() => {
        inputRef.current.focus({ cursor: 'end' });
    }, []);

    const initialValues = { username: '' };

    const formAttrs = {
        username: {
            name: 'username',
            label: t`Username`,
            rules: [FormUtil.ruleRequired()]
        }
    };
    return (
        <Form
            name={formName}
            form={form}
            labelCol={{ span: 6 }}
            wrapperCol={{ span: 18 }}
            initialValues={{ ...initialValues }}
            onFinish={(payload) => {
                setBasicAuthUsername(payload.username);
                FormUtil.submit(otpUrls.sendResetPwdOtp, payload)
                    .then((data) => {
                        setBasicAuthVerifId(data.verify_id);
                        onChange(data.verify_id, payload.username);
                    })
                    .catch(FormUtil.setFormErrors(form));
            }}
        >
            <Form.Item {...formAttrs.username}>
                <Input ref={inputRef} />
            </Form.Item>
        </Form>
    );
}

SendResetPwdOtpForm.displayName = formName;
SendResetPwdOtpForm.formName = formName;
