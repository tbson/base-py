import * as React from 'react';
import StorageUtil from 'service/helper/storage_util';
import UserProfile from 'component/account/user/profile';
import { ProfileType } from 'component/account/const';

export default function Profile() {
    const profileTYpe = StorageUtil.getProfileType();
    if ([ProfileType.user, ProfileType.ADMIN].includes(profileTYpe)) {
        return <UserProfile />;
    }
    return null;
}

Profile.displayName = 'Profile';
