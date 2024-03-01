import * as React from 'react';
import { useRef, useEffect } from 'react';
import { useRecoilValue } from 'recoil';
import { Form, Input } from 'antd';
import Util from 'service/helper/util';
import RequestUtil from 'service/helper/request_util';
import FormUtil from 'service/helper/form_util';
import TransferInput from 'component/common/form/ant/input/transfer_input.jsx';
import SelectInput from 'component/common/form/ant/input/select_input';
import { urls, labels, emptyRecord } from '../config';
import { roleOptionSt } from '../state';

/**
 * @callback FormCallback
 *
 * @param {Object} data
 * @param {number} id
 */

export class Service {
    /**
     * handleSubmit.
     *
     * @param {FormCallback} onChange
     * @param {number} id
     */
    static handleSubmit(onChange, id) {
        return (data, formikBag) => {
            Util.toggleGlobalLoading();
            const endPoint = id ? `${urls.crud}${id}` : urls.crud;
            const method = id ? 'put' : 'post';
            RequestUtil.apiCall(endPoint, data, method)
                .then((resp) => {
                    const { data } = resp;
                    onChange(data, id);
                })
                .catch((err) => {
                    const errors = err.response.data;
                    const formatedErrors = Util.setFormErrors(errors);
                    formikBag.setErrors(formatedErrors);
                })
                .finally(() => Util.toggleGlobalLoading(false));
        };
    }
}

const formName = 'RoleForm';

/**
 * RoleForm.
 *
 * @param {Object} props
 * @param {Object} props.data
 * @param {FormCallback} props.onChange
 * @param {Object} props.formRef
 */
export default function RoleForm({ data, onChange }) {
    const inputRef = useRef(null);
    const [form] = Form.useForm();
    const roleOption = useRecoilValue(roleOptionSt);

    useEffect(() => {
        inputRef.current.focus({ cursor: 'end' });
    }, []);

    const initValues = Util.isEmpty(data) ? emptyRecord : data;
    const id = initValues.id;
    const url = id ? `${urls.crud}${id}` : urls.crud;
    const method = id ? 'put' : 'post';

    const formAttrs = {
        title: {
            name: 'title',
            label: labels.title,
            rules: [FormUtil.ruleRequired()]
        },
        profile_type: {
            name: 'profile_type',
            label: labels.profile_type,
            rules: [FormUtil.ruleRequired()]
        },
        pem_ids: {
            name: 'pem_ids',
            label: labels.pem_ids,
            rules: [FormUtil.ruleRequired()]
        }
    };

    return (
        <Form
            form={form}
            name={formName}
            layout="vertical"
            initialValues={{ ...initValues }}
            onFinish={(payload) =>
                FormUtil.submit(url, payload, method)
                    .then((data) => onChange(data, id))
                    .catch(FormUtil.setFormErrors(form))
            }
        >
            <Form.Item {...formAttrs.title}>
                <Input ref={inputRef} />
            </Form.Item>
            <Form.Item {...formAttrs.profile_type}>
                <SelectInput block options={roleOption.profile_type} />
            </Form.Item>
            <Form.Item {...formAttrs.pem_ids}>
                <TransferInput options={roleOption.pem} />
            </Form.Item>
        </Form>
    );
}

RoleForm.displayName = formName;
RoleForm.formName = formName;
