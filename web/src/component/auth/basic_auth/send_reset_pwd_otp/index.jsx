import * as React from 'react';
import { useState, useEffect, useRef } from 'react';
import { t } from 'ttag';
import { Modal } from 'antd';
import Util from 'service/helper/util';
import Form from './form';

export class Service {
    static get toggleEvent() {
        return 'TOGGLE_SEND_RESET_PASSWORD_OTP_DIALOG';
    }

    static toggle(open = true) {
        Util.event.dispatch(Service.toggleEvent, { open });
    }
}

/**
 * @callback FormCallback
 * @param {string} verify_id
 * @param {string} username
 */

/**
 * SendResetPwdOtp.
 *
 * @param {Object} props
 * @param {FormCallback} props.onChange
 */
export default function SendResetPwdOtp({ onChange }) {
    const formRef = useRef();
    const [open, setOpen] = useState(false);

    const handleToggle = ({ detail: { open } }) => setOpen(open);

    useEffect(() => {
        Util.event.listen(Service.toggleEvent, handleToggle);
        return () => {
            Util.event.remove(Service.toggleEvent, handleToggle);
        };
    }, []);

    return (
        <Modal
            keyboard={false}
            maskClosable={false}
            destroyOnClose
            open={open}
            okButtonProps={{ form: Form.formName, key: 'submit', htmlType: 'submit' }}
            onCancel={() => Service.toggle(false)}
            okText={t`Reset password`}
            cancelText={t`Cancel`}
            title={t`Reset password`}
        >
            <Form
                onChange={(verifyId, username) => {
                    setOpen(false);
                    onChange(verifyId, username);
                }}
                formRef={formRef}
            />
        </Modal>
    );
}

SendResetPwdOtp.displayName = 'SendResetPwdOtp';
SendResetPwdOtp.toggle = Service.toggle;
