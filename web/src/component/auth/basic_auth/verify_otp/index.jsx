import * as React from 'react';
import { useState, useEffect } from 'react';
import { useRecoilValue } from 'recoil';
import { t } from 'ttag';
import { Modal, Button, Form, notification } from 'antd';
import Util from 'service/helper/util';
import RequestUtil from 'service/helper/request_util';
import { otpUrls } from 'component/auth/basic_auth/config';
import { basicAuthVerifyIdSt } from '../state';
import VerifyOtpForm from './form';

export class Service {
    static get toggleEvent() {
        return 'TOGGLE_VERIFY_OTP_DIALOG';
    }

    static toggle(open = true) {
        Util.event.dispatch(Service.toggleEvent, { open });
    }
}

/**
 * @callback onChange
 * @param {string} verify_id
 */

/**
 * VerifyOtp.
 *
 * @param {Object} props
 * @param {onChange} props.onChange
 *
 */
export default function VerifyOtp({ onChange }) {
    const [open, setOpen] = useState(false);
    const [form] = Form.useForm();
    const verifyId = useRecoilValue(basicAuthVerifyIdSt);

    const handleToggle = ({ detail: { open } }) => {
        setOpen(open);
    };

    useEffect(() => {
        Util.event.listen(Service.toggleEvent, handleToggle);
        return () => {
            Util.event.remove(Service.toggleEvent, handleToggle);
        };
    }, []);

    function resendOtp() {
        Util.toggleGlobalLoading();
        RequestUtil.apiCall(otpUrls.resendOtp, { verify_id: verifyId }, 'POST')
            .then(() => {
                notification.success({
                    message: t`OTP resent`,
                    description: t`Please check your email for the new OTP`,
                    duration: 8
                });
            })
            .catch((err) => {
                const errors = err.response.data;
                notification.error({
                    message: t`Error`,
                    description: errors.detail[0],
                    duration: 8
                });
            })
            .finally(() => {
                Util.toggleGlobalLoading(false);
            });
    }

    return (
        <Modal
            keyboard={false}
            maskClosable={false}
            destroyOnClose
            open={open}
            onCancel={() => Service.toggle(false)}
            title={t`Verify OTP`}
            footer={[
                <Button
                    key="1"
                    type="link"
                    onClick={() => resendOtp()}
                >{t`Resend OTP`}</Button>,
                <Button
                    key="2"
                    onClick={() => Service.toggle(false)}
                >{t`Cancel`}</Button>,
                <Button
                    key="submit"
                    type="primary"
                    htmlType="submit"
                    onClick={() => form.submit()}
                >
                    {t`Verify OTP`}
                </Button>
            ]}
        >
            <VerifyOtpForm
                form={form}
                onChange={(verifyCode) => {
                    setOpen(false);
                    onChange(verifyCode);
                }}
            />
        </Modal>
    );
}

VerifyOtp.displayName = 'VerifyOtp';
VerifyOtp.toggle = Service.toggle;
