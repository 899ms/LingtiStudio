"use client";

import { Button, Card, Col, Descriptions, Progress, Row, Space, Steps, Tag, Timeline, Typography } from "antd";
import { DownloadOutlined, PlayCircleOutlined, ReloadOutlined, SaveOutlined } from "@ant-design/icons";

const scenes = [
  ["开场介绍", "镜头展示现代化养老社区外观，旁白介绍智慧康养服务。"],
  ["服务展示", "展示居住空间、休闲区和健康管理设备，突出舒适、安全、智能。"],
  ["成片收束", "老人参与休闲活动，画面转入品牌结束页和服务口号。"],
];

export default function DemoPage() {
  return (
    <Space direction="vertical" size={24} style={{ width: "100%" }}>
      <div className="workspace-header">
        <div className="workspace-title">
          <Typography.Title level={2}>任务详情 · 智慧康养宣传片</Typography.Title>
          <Typography.Paragraph type="secondary">
            展示视频任务的分镜审核、生成进度、运行日志和成片交付状态。
          </Typography.Paragraph>
        </div>
        <Space>
          <Tag color="processing">视频生成中</Tag>
          <Tag color="blue">1080p</Tag>
          <Tag color="cyan">9:16</Tag>
        </Space>
      </div>

      <Card className="lingti-card" title="流程进度">
        <Space direction="vertical" size={18} style={{ width: "100%" }}>
          <Steps
            current={5}
            items={[
              { title: "脚本" },
              { title: "审核" },
              { title: "资产" },
              { title: "关键帧" },
              { title: "配音" },
              { title: "视频" },
              { title: "组装" },
              { title: "完成" },
            ]}
          />
          <Progress percent={72} status="active" />
        </Space>
      </Card>

      <Row gutter={[24, 24]}>
        <Col xs={24} xl={15}>
          <Card className="lingti-card" title="脚本审核与分镜">
            <Space direction="vertical" size={16} style={{ width: "100%" }}>
              {scenes.map(([title, text], index) => (
                <Card key={title} size="small" className="lingti-mini-card">
                  <Space direction="vertical" size={8} style={{ width: "100%" }}>
                    <Space>
                      <Tag color="blue">Scene {index + 1}</Tag>
                      <Typography.Text strong>{title}</Typography.Text>
                    </Space>
                    <Typography.Paragraph style={{ marginBottom: 0 }}>{text}</Typography.Paragraph>
                    <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
                      画面提示词：高端商业宣传片风格，暖色自然光，人物真实，镜头平稳。
                    </Typography.Paragraph>
                  </Space>
                </Card>
              ))}
              <Space>
                <Button type="primary" icon={<SaveOutlined />}>保存脚本</Button>
                <Button icon={<PlayCircleOutlined />}>审核通过并继续</Button>
              </Space>
            </Space>
          </Card>
        </Col>
        <Col xs={24} xl={9}>
          <Space direction="vertical" size={24} style={{ width: "100%" }}>
            <Card className="lingti-card" title="任务信息">
              <Descriptions column={1} size="small">
                <Descriptions.Item label="任务编号">demo-20260622-001</Descriptions.Item>
                <Descriptions.Item label="当前阶段">视频片段生成</Descriptions.Item>
                <Descriptions.Item label="视频引擎">Kling / MiniMax Video 多链路可选</Descriptions.Item>
                <Descriptions.Item label="字幕">已开启</Descriptions.Item>
                <Descriptions.Item label="目标时长">60 秒</Descriptions.Item>
              </Descriptions>
            </Card>
            <Card className="lingti-card" title="生成日志">
              <Timeline
                items={[
                  { color: "green", children: "脚本生成完成，等待审核" },
                  { color: "green", children: "人物、场景、道具资产已生成" },
                  { color: "green", children: "关键帧与配音文件已生成" },
                  { color: "blue", children: "正在生成第 3 段视频片段" },
                ]}
              />
            </Card>
          </Space>
        </Col>
      </Row>

      <Card className="lingti-card" title="成片结果">
        <Row gutter={[24, 24]} align="middle">
          <Col xs={24} lg={10}>
            <div className="demo-video-preview">
              <PlayCircleOutlined />
              <span>成片预览</span>
            </div>
          </Col>
          <Col xs={24} lg={14}>
            <Space direction="vertical" size={14}>
              <Typography.Paragraph>
                系统完成组装后，可在此预览视频、下载无字幕版、下载带字幕版，并导出剪映草稿。
              </Typography.Paragraph>
              <Space wrap>
                <Button icon={<DownloadOutlined />}>下载无字幕版</Button>
                <Button icon={<DownloadOutlined />}>下载带字幕版</Button>
                <Button icon={<DownloadOutlined />}>下载剪映草稿</Button>
                <Button icon={<ReloadOutlined />}>重新组装</Button>
              </Space>
            </Space>
          </Col>
        </Row>
      </Card>
    </Space>
  );
}
