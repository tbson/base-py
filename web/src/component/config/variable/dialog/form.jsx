import * as React from 'react';
import { useRef, useEffect } from 'react';
import { useRecoilValue } from 'recoil';
import { Form, Input } from 'antd';
import Util from 'service/helper/util';
import FormUtil from 'service/helper/form_util';
import SelectInput from 'component/common/form/ant/input/select_input';
import { urls, labels } from '../config';
import { variableOptionSt } from '../state';

const { TextArea } = Input;

const formName = 'VariableForm';
const emptyRecord = {
    id: 0,
    uid: '',
    value: '',
    description: '',
    type: 1
};

/**
 * @callback FormCallback
 *
 * @param {Object} data
 * @param {number} id
 */

/**
 * VariableForm.
 *
 * @param {Object} props
 * @param {Object} props.data
 * @param {FormCallback} props.onChange
 */
export default function VariableForm({ data, onChange }) {
    const inputRef = useRef(null);
    const [form] = Form.useForm();
    const variableOption = useRecoilValue(variableOptionSt);

    const initialValues = Util.isEmpty(data) ? emptyRecord : data;
    const id = initialValues.id;

    const endPoint = id ? `${urls.crud}${id}` : urls.crud;
    const method = id ? 'put' : 'post';

    const formAttrs = {
        uid: {
            name: 'uid',
            label: labels.uid,
            rules: [FormUtil.ruleRequired()]
        },
        value: {
            name: 'value',
            label: labels.value,
            rules: [FormUtil.ruleRequired()]
        },
        description: {
            name: 'description',
            label: labels.description
        },
        type: {
            name: 'type',
            label: labels.type,
            rules: [FormUtil.ruleRequired()]
        }
    };

    useEffect(() => {
        inputRef.current.focus({ cursor: 'end' });
    }, []);

    return (
        <Form
            form={form}
            name={formName}
            labelCol={{ span: 6 }}
            wrapperCol={{ span: 18 }}
            initialValues={{ ...initialValues }}
            onFinish={(payload) =>
                FormUtil.submit(endPoint, payload, method)
                    .then((data) => onChange(data, id))
                    .catch(FormUtil.setFormErrors(form))
            }
        >
            <Form.Item {...formAttrs.uid}>
                <Input ref={inputRef} />
            </Form.Item>

            <Form.Item {...formAttrs.value}>
                <Input />
            </Form.Item>

            <Form.Item {...formAttrs.description}>
                <TextArea />
            </Form.Item>

            <Form.Item {...formAttrs.type}>
                <SelectInput block options={variableOption.type} />
            </Form.Item>
        </Form>
    );
}

VariableForm.displayName = formName;
VariableForm.formName = formName;
