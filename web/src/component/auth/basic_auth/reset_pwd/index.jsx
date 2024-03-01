import * as React from 'react';
import { useState, useEffect } from 'react';
import { t } from 'ttag';
import { Modal } from 'antd';
import Util from 'service/helper/util';
import Form from './form';

export class Service {
    static get toggleEvent() {
        return 'TOGGLE_RESET_PASSWORD_DIALOG';
    }

    static toggle(open = true) {
        Util.event.dispatch(Service.toggleEvent, {
            open
        });
    }
}

export default function ResetPwd() {
    const [open, setOpen] = useState(false);

    const handleToggle = ({ detail: { open } }) => {
        setOpen(open);
    };

    useEffect(() => {
        Util.event.listen(Service.toggleEvent, handleToggle);
        return () => {
            Util.event.remove(Service.toggleEvent, handleToggle);
        };
    }, []);

    return (
        <Modal
            destroyOnClose={true}
            open={open}
            okButtonProps={{ form: Form.formName, key: 'submit', htmlType: 'submit' }}
            okText="OK"
            onCancel={() => Service.toggle(false)}
            cancelText={t`Cancel`}
            title={t`Reset password`}
        >
            <Form
                onChange={() => {
                    setOpen(false);
                }}
            />
        </Modal>
    );
}

ResetPwd.displayName = 'ResetPwd';
ResetPwd.toggle = Service.toggle;
