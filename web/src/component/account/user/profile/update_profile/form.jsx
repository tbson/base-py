import * as React from 'react';
import { useRef, useEffect } from 'react';
import { t } from 'ttag';
import { Form, Input } from 'antd';
import FormUtil from 'service/helper/form_util';
import { profileUrls } from 'component/account/user/config';

const formName = 'UpdateProfileForm';

export default function UpdateProfileForm({ data, onChange }) {
    const inputRef = useRef(null);
    const [form] = Form.useForm();

    useEffect(() => {
        inputRef.current.focus({ cursor: 'end' });
    }, []);

    const formAttrs = {
        mobile: {
            name: 'mobile',
            label: t`Phone number`
        },
        first_name: {
            name: 'first_name',
            label: t`First name`,
            rules: [FormUtil.ruleRequired()]
        },
        last_name: {
            name: 'last_name',
            label: t`Last name`,
            rules: [FormUtil.ruleRequired()]
        }
    };

    return (
        <Form
            form={form}
            name={formName}
            labelCol={{ span: 6 }}
            wrapperCol={{ span: 18 }}
            initialValues={{ ...data }}
            onFinish={(payload) =>
                FormUtil.submit(profileUrls.profile, payload, 'put')
                    .then((data) => onChange(data))
                    .catch(FormUtil.setFormErrors(form))
            }
        >
            <Form.Item {...formAttrs.mobile}>
                <Input ref={inputRef} />
            </Form.Item>
            <Form.Item {...formAttrs.first_name}>
                <Input />
            </Form.Item>
            <Form.Item {...formAttrs.last_name}>
                <Input />
            </Form.Item>
        </Form>
    );
}

UpdateProfileForm.displayName = formName;
UpdateProfileForm.formName = formName;
