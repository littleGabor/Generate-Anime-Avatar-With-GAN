import logo from './logo.svg';
import './App.css';
// src/App.js
import React from 'react';
import { Link } from 'react-router-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Breadcrumb, Layout, Menu, theme } from 'antd';
import History from './History';
import UpdateConfigComponent from './UpdateConfigComponent';
import Like from "./Like";


const { Header, Content, Footer } = Layout;
const items = [
    { key: 1, label: '主页', url: '/' },
    { key: 2, label: '历史图片', url: '/history' },
    { key: 3, label: '我喜欢的图片', url: '/like' },
    
  ];

function App() {
    const {
        token: { colorBgContainer, borderRadiusLG },
      } = theme.useToken();
    return (
        <Router>
        <Layout>
            <Header
            style={{
                display: 'flex',
                alignItems: 'center',
            }}
            >
            <div className="demo-logo" />
            <Menu
                theme="dark"
                mode="horizontal"
                items={items.map(item => ({
                ...item,
                label: (
                    <Link to={item.url} style={{ color: 'inherit', textDecoration: 'none' }}>
                    {item.label}
                    </Link>
                )
                }))}
                style={{
                flex: 1,
                minWidth: 0,
                }}
            />
            </Header>
            <Content
            style={{
                padding: '0 48px',
            }}
            >
            <Breadcrumb
                style={{
                margin: '30px 0',
                }}
                items={[
                    { }
                ]}
            >
               
                
            </Breadcrumb>
            <div
                style={{
                background: colorBgContainer,
                minHeight: 800,
                padding: 24,
                borderRadius: borderRadiusLG,
                }}
            >
            
                <Routes>
                <Route path="/" element={<UpdateConfigComponent />} />
                <Route path="/history" element={<History />} />
                <Route path="/like" element={<Like />} />
                </Routes>
            
            </div>
            </Content>
            <Footer
            style={{
                textAlign: 'center',
            }}
            >
            GJB ©{new Date().getFullYear()} Created by Love
            </Footer>
        
            
        </Layout>
        </Router>
    );
}

export default App;

