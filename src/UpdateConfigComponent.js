// src/UpdateConfigComponent.js
import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Button, Slider } from 'antd';
import { Image } from 'antd';

function UpdateConfigComponent() {
    axios.defaults.baseURL = 'http://localhost:5000'; // 根据需要设置你的后端地址
    const param = 'gen_num'; // 固定参数为 "gen_num"
    const [value, setValue] = useState('');
    const [imageBase64, setImageBase64] = useState(''); // 用于存储接收的图像Base64编码

    const updateConfig = () => {
        const newConfig = { [param]: value };
        axios.post('/update-config', { new_config: newConfig })
            .then(response => {
                console.log(response.data);
                // 如果响应包含Base64编码的图像，则将其存储在状态中
                if (response.data.image_base64) {
                    setImageBase64(response.data.image_base64);
                }
            })
            .catch(error => {
                console.error('Error updating config:', error);
            });
    };

    // 定义下拉列表的选项
    // const valueOptions = [
    //     { value: '1', label: '1' },
    //     { value: '2', label: '2' },
    //     { value: '3', label: '3' },
    //     // 可以根据需要添加更多选项
    // ];

    return (
        <div>
            <h2>Update Config</h2>
            {/* 固定param为 "gen_num" */}
            <p>Parameter: {param}</p>
            {/* 使用下拉列表选择value */}
            {/* <select value={value} onChange={e => setValue(e.target.value)}>
                <option value="">请选择</option>
                {valueOptions.map(option => (
                    <option key={option.value} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select> */}
             <Slider
                min={1} // 设置最小值
                max={10} // 设置最大值
                step={1} // 设置步长
                value={value} // 设置当前值
                onChange={setValue} // 设置值改变时的回调函数
                style={{ width: '20%' }}
            />
            <Button type="primary" onClick={updateConfig}>生成</Button>

            {/* 如果有图像，则在页面上显示 */}
            {imageBase64 && (
                <div>
                    <h3>Generated Image:</h3>
                    <Image width={200} src={`data:image/png;base64,${imageBase64}`} alt="Generated" />
                </div>
            )}

            {/* 通过React Router的Link组件导航到HistoryImages页面 */}
            <div>
                <Link to="/history">
                <Button type="primary">查看历史图片</Button>
                </Link>
            </div>
        </div>
    );
}

export default UpdateConfigComponent;
