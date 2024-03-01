import * as React from "react";
import PageHeading from "component/common/page_heading";
import Table from "./table";
import { messages } from "./config";

export default function User() {
    return (
        <>
            <PageHeading>
                <>{messages.heading}</>
            </PageHeading>
            <Table />
        </>
    );
}

User.displayName = "User";
