"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button, Card, Checkbox, Form, Input, Space, Typography, message } from "antd";
import { LockOutlined, LoginOutlined, UserOutlined } from "@ant-design/icons";

export default function LoginPage() {
  const router = useRouter();
  const [messageApi, contextHolder] = message.useMessage();

  function handleLogin(values: { username: string; password: string; remember?: boolean }) {
    if (!values.username || !values.password) {
      messageApi.warning("请输入账号和密码");
      return;
    }
    window.localStorage.setItem(
      "lingti.auth",
      JSON.stringify({ username: values.username, remember: Boolean(values.remember), loginAt: new Date().toISOString() })
    );
    messageApi.success("登录成功");
    router.push("/");
  }

  return (
    <div className="auth-panel">
      {contextHolder}
      <Card className="lingti-card auth-card">
        <Space direction="vertical" size={24} style={{ width: "100%" }}>
          <div className="workspace-title">
            <Typography.Text type="secondary">Lingti Video Platform</Typography.Text>
            <Typography.Title level={2}>灵缇多链路平台AI视频在线制作平台</Typography.Title>
            <Typography.Paragraph type="secondary">
              登录后进入 AI 视频在线制作工作台，管理视频任务、素材、审核、恢复和成片交付。
            </Typography.Paragraph>
          </div>
          <Form
            layout="vertical"
            initialValues={{ username: "admin", remember: true }}
            onFinish={handleLogin}
          >
            <Form.Item name="username" label="账号" rules={[{ required: true, message: "请输入账号" }]}>
              <Input prefix={<UserOutlined />} placeholder="admin" size="large" />
            </Form.Item>
            <Form.Item name="password" label="密码" rules={[{ required: true, message: "请输入密码" }]}>
              <Input.Password prefix={<LockOutlined />} placeholder="请输入登录密码" size="large" />
            </Form.Item>
            <Form.Item name="remember" valuePropName="checked">
              <Checkbox>记住登录状态</Checkbox>
            </Form.Item>
            <Button type="primary" htmlType="submit" icon={<LoginOutlined />} size="large" block>
              登录
            </Button>
          </Form>
          <Link href="/">
            <Button block>返回平台首页</Button>
          </Link>
        </Space>
      </Card>
    </div>
  );
}
