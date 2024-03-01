import * as React from 'react';
import { Row, Col } from 'antd';
import { t } from 'ttag';

export default function ProfileSummary(data) {
    return (
        <table className="styled-table">
            <tbody>
                <tr>
                    <td span={6}>
                        <strong>{t`Email`}</strong>
                    </td>
                    <td span={18}>{data.email}</td>
                </tr>
                <tr>
                    <td span={6}>
                        <strong>{t`Phone number`}</strong>
                    </td>
                    <td span={18}>{data.mobile}</td>
                </tr>
                <tr>
                    <td span={6}>
                        <strong>{t`Fullname`}</strong>
                    </td>
                    <td span={18}>{data.full_name}</td>
                </tr>
            </tbody>
        </table>
    );
}
ProfileSummary.displayName = 'ProfileSummary';
