import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Image } from 'antd';
const HistoryImages = () => {
  axios.defaults.baseURL = 'http://localhost:5000';
  const [images, setImages] = useState([]);
   
  useEffect(() => {
    // 发送请求获取历史图片数据
    axios.get('/history')
      .then(response => {
        setImages(response.data);
      })
      .catch(error => {
        console.error('Error fetching history images:', error);
      });
  }, []);
  const handleClearHistory = () => {
    axios.delete('/clear-history')
      .then(response => {
        setImages([]);
        console.log('History cleared successfully');
      })
      .catch(error => {
        console.error('Error clearing history:', error);
      });
  };

  return (
    <div>
      <h1>历史图片</h1>
      <button onClick={handleClearHistory}>清除历史图片</button>
      <div className="image-container">
        {images.map((image, index) => (
          <div key={index} className="image-item">
            <Image width={200} src={`data:image/png;base64,${image.base64}`} alt={`Image ${index}`} />
            {/* 如果需要添加更多交互，可以在这里添加 */}
          </div>
        ))}
      </div>
    </div>
  );
}

export default HistoryImages;