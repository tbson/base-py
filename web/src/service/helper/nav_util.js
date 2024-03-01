import Util from 'service/helper/util';
import StorageUtil from 'service/helper/storage_util';
import RequestUtil from 'service/helper/request_util';

export default class NavUtil {
    /**
     * navigateTo.
     *
     * @param {Navigate} navigate
     */
    static navigateTo(navigate) {
        return (url = '/') => {
            navigate(url);
        };
    }

    /**
     * logout.
     *
     * @param {Navigate} navigate
     */
    static logout(navigate) {
        return () => {
            const baseUrl = RequestUtil.getApiBaseUrl();
            const logoutUrl = `${baseUrl}auth/common-auth/logout/`;
            Util.toggleGlobalLoading();
            RequestUtil.apiCall(logoutUrl, {}, 'POST')
                .then(() => {
                    NavUtil.cleanAndMoveToLoginPage(navigate);
                })
                .finally(() => {
                    Util.toggleGlobalLoading(false);
                });
        };
    }

    /**
     * cleanAndMoveToLoginPage.
     *
     * @param {Navigate} navigate
     * @returns {void}
     */
    static cleanAndMoveToLoginPage(navigate) {
        const currentUrl = window.location.href.split('#')[1];
        StorageUtil.removeStorage('auth');
        let loginUrl = '/login';
        if (currentUrl) {
            loginUrl = `${loginUrl}?next=${currentUrl}`;
        }
        if (navigate) {
            NavUtil.navigateTo(navigate)(loginUrl);
        } else {
            window.location.href = `/#${loginUrl}`;
        }
    }
}
