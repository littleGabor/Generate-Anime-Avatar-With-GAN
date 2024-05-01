import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Image } from 'antd';
import { Button } from 'antd';
const LikeImages = () => {
  axios.defaults.baseURL = 'http://localhost:5000';
  const [images, setImages] = useState([]);
   
  useEffect(() => {
    // 发送请求获取历史图片数据
    axios.get('/like')
      .then(response => {
        setImages(response.data);
      })
      .catch(error => {
        console.error('Error fetching history images:', error);
      });
  }, []);
  const handleClearLike = () => {
    axios.delete('/clear-like')
      .then(response => {
        setImages([]);
        console.log('Like cleared successfully');
      })
      .catch(error => {
        console.error('Error clearing like:', error);
      });
  };

  return (
    <div>
      <h1>我喜欢的图片</h1>
      <Button type="primary" onClick={handleClearLike}>清除图片</Button>
      <div className="image-container">
        {images.map((image, index) => (
          <div key={index} className="image-item">
            <Image width={200} src={`data:image/png;base64,${image.base64}`} alt={`Image ${index}`} />
          </div>
        ))}
      </div>
    </div>
  );
}
export default LikeImages;