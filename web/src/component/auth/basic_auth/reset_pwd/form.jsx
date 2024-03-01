import * as React from 'react';
import { useRef, useEffect } from 'react';
import { useRecoilValue } from 'recoil';
import { t } from 'ttag';
import { Form, Input } from 'antd';
import FormUtil from 'service/helper/form_util';
import { urls } from '../config';
import {
    basicAuthUsernameSt,
    basicAuthVerifyIdSt,
    basicAuthVerifyCodeSt
} from '../state';

const formName = 'ResetPwdForm';

/**
 * ResetPwdForm.
 *
 * @param {Object} props
 * @param {function} props.onChange
 */
export default function ResetPwdForm({ onChange }) {
    const inputRef = useRef(null);
    const [form] = Form.useForm();

    const username = useRecoilValue(basicAuthUsernameSt);
    const verifyId = useRecoilValue(basicAuthVerifyIdSt);
    const verifyCode = useRecoilValue(basicAuthVerifyCodeSt);

    useEffect(() => {
        inputRef.current.focus({ cursor: 'end' });
    }, []);

    const initialValues = { password: '', password_confirm: '' };
    const formAttrs = {
        password: {
            name: 'password',
            label: t`Password`,
            rules: [FormUtil.ruleRequired()]
        },
        password_confirm: {
            name: 'password_confirm',
            label: t`Password confirm`,
            rules: [FormUtil.ruleRequired()]
        }
    };

    return (
        <Form
            form={form}
            name={formName}
            labelCol={{ span: 8 }}
            wrapperCol={{ span: 16 }}
            initialValues={{ ...initialValues }}
            onFinish={(payload) =>
                FormUtil.submit(urls.resetPwd, {
                    ...payload,
                    username,
                    verify_id: verifyId,
                    verify_code: verifyCode
                })
                    .then((data) => onChange(data))
                    .catch(FormUtil.setFormErrors(form))
            }
        >
            <Form.Item {...formAttrs.password}>
                <Input ref={inputRef} type="password" />
            </Form.Item>

            <Form.Item {...formAttrs.password_confirm}>
                <Input type="password" />
            </Form.Item>
        </Form>
    );
}

ResetPwdForm.displayName = formName;
ResetPwdForm.formName = formName;
