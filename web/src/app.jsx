import * as React from 'react';
import { useEffect, useState } from 'react';
import { useRecoilState } from 'recoil';
import { useLocale } from 'ttag';
import { App, ConfigProvider } from 'antd';
import { Outlet } from 'react-router-dom';
import { localeSt } from 'src/state';
import Spinner from 'component/common/spinner';
import Util from 'service/helper/util';
import LocaleUtil from 'service/helper/locale_util';

Util.responseIntercept();

export default function MainApp() {
    const [dataLoaded, setDataLoaded] = useState(false);
    const [locale, setLocale] = useRecoilState(localeSt);
    useLocale(locale);
    useEffect(() => {
        LocaleUtil.fetchLocales().then(() => {
            setDataLoaded(true);
            setLocale(LocaleUtil.setLocale(locale));
        });
    }, []);
    if (!dataLoaded) {
        return <div>Loading...</div>;
    }
    return (
        <div key={locale}>
            <ConfigProvider theme={{ components: { Menu: { itemHeight: 34 } } }}>
                <App>
                    <Spinner />
                    <Outlet />
                </App>
            </ConfigProvider>
        </div>
    );
}
