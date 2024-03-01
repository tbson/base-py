import * as React from 'react';
import { useRef, useEffect } from 'react';
import { Button, Row, Col, Form, Input } from 'antd';
import { t } from 'ttag';
import { CheckOutlined } from '@ant-design/icons';
import FormUtil from 'service/helper/form_util';
import { urls } from '../config';

const formName = 'LoginForm';

export default function LoginForm({ onChange, children }) {
    const inputRef = useRef(null);
    const [form] = Form.useForm();

    useEffect(() => {
        inputRef.current.focus({ cursor: 'end' });
    }, []);

    const initialValues = {
        username: '',
        password: ''
    };

    const formAttrs = {
        username: {
            name: 'username',
            label: t`Username`,
            rules: [FormUtil.ruleRequired()]
        },
        password: {
            name: 'password',
            label: t`Password`,
            rules: [FormUtil.ruleRequired()]
        }
    };

    return (
        <Form
            form={form}
            labelCol={{ span: 8 }}
            wrapperCol={{ span: 16 }}
            initialValues={{ ...initialValues }}
            onFinish={(payload) =>
                FormUtil.submit(urls.login, payload)
                    .then((data) => onChange(data))
                    .catch(FormUtil.setFormErrors(form))
            }
        >
            <Form.Item {...formAttrs.username}>
                <Input ref={inputRef} />
            </Form.Item>

            <Form.Item {...formAttrs.password}>
                <Input type="password" />
            </Form.Item>

            <br />
            <Row>
                <Col span={12}>{children}</Col>
                <Col span={12} className="right">
                    <Button type="primary" htmlType="submit" icon={<CheckOutlined />}>
                        {t`Login`}
                    </Button>
                </Col>
            </Row>
        </Form>
    );
}
LoginForm.displayName = formName;
LoginForm.formName = formName;
