import * as React from 'react';
import { useState } from 'react';
import { PlusOutlined } from '@ant-design/icons';
import { Upload } from 'antd';

const getBase64 = (img, callback) => {
    const reader = new FileReader();
    reader.addEventListener('load', () => callback(reader.result));
    reader.readAsDataURL(img);
};

/**
 * DateInput.
 *
 * @param {Object} props
 * @param {string} props.value
 * @param {function} props.onChange
 * @param {string} props.label
 * @returns {ReactElement}
 */
export default function ImageInput({ value, onChange }) {
    console.log(value)
    const [imageUrl, setImageUrl] = useState(value);
    const uploadButton = (
        <button
            style={{
                border: 0,
                background: 'none'
            }}
            type="button"
        >
            <PlusOutlined />
            <div
                style={{
                    marginTop: 8
                }}
            >
                Upload
            </div>
        </button>
    );

    const handleChange = (file) => {
        onChange(file);
        getBase64(file, (imageUrl) => {
            setImageUrl(imageUrl);
        });
        return false;
    }

    return (
        <Upload
            name="avatar"
            listType="picture-card"
            className="avatar-uploader"
            showUploadList={false}
            beforeUpload={handleChange}
        >
            {imageUrl ? (
                <img
                    src={imageUrl}
                    alt="avatar"
                    style={{
                        width: '100%'
                    }}
                />
            ) : (
                uploadButton
            )}
        </Upload>
    );
}
