import * as React from 'react';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { t } from 'ttag';
import { Row, Col, Card, Button } from 'antd';
import NavUtil from 'service/helper/nav_util';
import StorageUtil from 'service/helper/storage_util';
import LocaleSelect from 'component/common/locale_select.jsx';
import Form from './form';
import VerifyOtp from '../verify_otp';
import SendResetPwdOtp from '../send_reset_pwd_otp';
import ResetPwd from '../reset_pwd';

const styles = {
    wrapper: {
        marginTop: 20
    }
};
export default function Login() {
    const navigate = useNavigate();
    const navigateTo = NavUtil.navigateTo(navigate);

    useEffect(() => {
        StorageUtil.getToken() && navigateTo();
    }, []);

    function handleLogin(data) {
        const nextUrl = window.location.href.split('next=')[1] || '/';
        StorageUtil.setStorage('auth', data);
        navigateTo(nextUrl);
    }

    function onSendResetPwdOtp() {
        VerifyOtp.toggle(true);
    }

    function onVerifyOtp() {
        ResetPwd.toggle(true);
    }

    return (
        <div>
            <div className="right content">
                <LocaleSelect />
            </div>
            <Row>
                <Col
                    xs={{ span: 24 }}
                    md={{ span: 12, offset: 6 }}
                    lg={{ span: 8, offset: 8 }}
                >
                    <Card title={t`Login`} style={styles.wrapper}>
                        <Form onChange={handleLogin}>
                            <>
                                <Button
                                    type="link"
                                    onClick={() => SendResetPwdOtp.toggle()}
                                >
                                    {t`Forgot password`}
                                </Button>
                            </>
                        </Form>
                    </Card>
                </Col>
            </Row>
            <SendResetPwdOtp onChange={onSendResetPwdOtp} />
            <VerifyOtp onChange={onVerifyOtp} />
            <ResetPwd />
        </div>
    );
}
