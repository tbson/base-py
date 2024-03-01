import * as React from 'react';
import { useState, useEffect } from 'react';
import { useNavigate, useLocation, Outlet } from 'react-router-dom';
import { t } from 'ttag';
import { Layout, Menu, Row, Col, Button } from 'antd';
import {
    MenuUnfoldOutlined,
    MenuFoldOutlined,
    UserOutlined,
    TeamOutlined,
    LogoutOutlined,
    SettingFilled,
    TagsOutlined
} from '@ant-design/icons';
import { LOGO_TEXT, DOMAIN } from 'src/const';
import StorageUtil from 'service/helper/storage_util';
import PemUtil from 'service/helper/pem_util';
import NavUtil from 'service/helper/nav_util';
import LocaleSelect from 'component/common/locale_select.jsx';
import styles from './styles.module.css';

const { Header, Footer, Sider, Content } = Layout;

/**
 * MainLayout.
 */
export default function MainLayout() {
    const [menuItems, setMenuItems] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();

    const [collapsed, setCollapsed] = useState(false);
    const toggle = () => {
        setCollapsed(!collapsed);
    };

    useEffect(() => {
        setMenuItems(getMenuItems());
    }, []);

    const logout = NavUtil.logout(navigate);
    const navigateTo = NavUtil.navigateTo(navigate);

    /**
     * processSelectedKey.
     *
     * @param {string} pathname
     * @returns {string}
     */
    function processSelectedKey(pathname) {
        if (pathname.startsWith('/user')) return '/user';
        return pathname;
    }

    function getMenuItems() {
        const result = [];

        result.push({ label: t`Profile`, key: '/', icon: <UserOutlined /> });
        PemUtil.canView('variable') &&
            result.push({
                label: t`Variable`,
                key: '/config/variable',
                icon: <SettingFilled />
            });

        PemUtil.canView('user') &&
            result.push({
                label: t`User`,
                key: '/account/user',
                icon: <TeamOutlined />
            });
        PemUtil.canView('role') &&
            result.push({
                label: t`Role`,
                key: '/account/role',
                icon: <TagsOutlined />
            });
        return result;
    }

    return (
        <Layout hasSider className={styles.wrapperContainer}>
            <Sider
                trigger={null}
                breakpoint="lg"
                collapsedWidth="34"
                theme="dark"
                collapsible
                collapsed={collapsed}
                onBreakpoint={(broken) => {
                    setCollapsed(broken);
                }}
            >
                <div className="sider">
                    {collapsed || (
                        <div className="logo">
                            <div className="logo-text">{LOGO_TEXT}</div>
                        </div>
                    )}
                    <Menu
                        className="sidebar-nav"
                        defaultSelectedKeys={[processSelectedKey(location.pathname)]}
                        theme="dark"
                        mode="inline"
                        items={menuItems}
                        onSelect={({ key }) => navigateTo(key)}
                    />
                </div>
            </Sider>
            <Layout className="site-layout">
                <Header className="site-layout-header" style={{ padding: 0 }}>
                    <Row>
                        <Col span={12}>
                            {React.createElement(
                                collapsed ? MenuUnfoldOutlined : MenuFoldOutlined,
                                {
                                    className: 'trigger',
                                    onClick: toggle
                                }
                            )}
                        </Col>
                        <Col span={12} className="right" style={{ paddingRight: 5 }}>
                            <span>{StorageUtil.getStorageObj('auth').full_name}</span>
                            &nbsp;&nbsp;
                            <LocaleSelect />
                            &nbsp;&nbsp;
                            <Button icon={<LogoutOutlined />} onClick={logout} danger />
                        </Col>
                    </Row>
                </Header>
                <Content className="site-layout-content">
                    <Outlet />
                </Content>
                <Footer className="layout-footer">
                    <div className="layout-footer-text">
                        Copyright<sup>©</sup> {DOMAIN} {new Date().getFullYear()}
                    </div>
                </Footer>
            </Layout>
        </Layout>
    );
}
