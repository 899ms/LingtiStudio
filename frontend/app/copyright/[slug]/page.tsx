"use client";

import { useParams } from "next/navigation";
import { Alert, Button, Card, Col, Descriptions, Progress, Row, Space, Steps, Table, Tag, Timeline, Typography, Upload } from "antd";
import { DownloadOutlined, InboxOutlined, PlayCircleOutlined, ReloadOutlined, SaveOutlined, SoundOutlined } from "@ant-design/icons";

const pages = {
  voice: {
    title: "旁白音色选择",
    description: "选择视频旁白音色，支持语言、风格筛选和试听。",
    content: <VoiceContent />,
  },
  upload: {
    title: "参考素材上传",
    description: "上传人物图、产品图或参考视频，作为后续分析和生成参考。",
    content: <UploadContent />,
  },
  taskcenter: {
    title: "任务中心",
    description: "按状态集中管理进行中、失败待处理和已完成的视频项目。",
    content: <TaskCenterContent />,
  },
  script: {
    title: "脚本审核与分镜",
    description: "审核分镜标题、旁白文案和画面提示词，确认后继续生成。",
    content: <ScriptContent />,
  },
  progress: {
    title: "生成进度",
    description: "展示脚本、审核、资产、关键帧、配音、视频和组装进度。",
    content: <ProgressContent />,
  },
  logs: {
    title: "生成日志",
    description: "查看任务运行日志、阶段状态和异常提示。",
    content: <LogsContent />,
  },
  result: {
    title: "成片结果",
    description: "提供视频预览、无字幕版、带字幕版和剪映草稿下载入口。",
    content: <ResultContent />,
  },
  analysisResult: {
    title: "对标分析结果",
    description: "查看参考视频拆解后的人物、场景、节奏和提示词。",
    content: <AnalysisResultContent />,
  },
  config: {
    title: "编辑配置",
    description: "维护各类 AI provider、模型、密钥和默认音色。",
    content: <ConfigContent />,
  },
} as const;

type PageKey = keyof typeof pages;

export default function CopyrightPage() {
  const params = useParams<{ slug: string }>();
  const slug = params.slug;
  const page = pages[slug as PageKey];
  if (!page) {
    return null;
  }

  return (
    <Space direction="vertical" size={24} style={{ width: "100%" }}>
      <div className="workspace-header">
        <div className="workspace-title">
          <Typography.Title level={2}>{page.title}</Typography.Title>
          <Typography.Paragraph type="secondary">{page.description}</Typography.Paragraph>
        </div>
        <Tag color="blue">灵缇视频平台</Tag>
      </div>
      {page.content}
    </Space>
  );
}

function VoiceContent() {
  return (
    <Row gutter={[24, 24]}>
      <Col xs={24} xl={14}>
        <Card className="lingti-card" title="音色目录">
          <Table
            pagination={false}
            dataSource={[
              { key: "1", name: "清晰女声", lang: "zh-CN", tag: "广告 / 讲解", source: "system" },
              { key: "2", name: "沉稳男声", lang: "zh-CN", tag: "纪录片 / 企业", source: "system" },
              { key: "3", name: "活力青年", lang: "zh-CN", tag: "短视频 / 口播", source: "system" },
            ]}
            columns={[
              { title: "音色", dataIndex: "name" },
              { title: "语言", dataIndex: "lang" },
              { title: "风格标签", dataIndex: "tag" },
              { title: "来源", dataIndex: "source" },
            ]}
          />
        </Card>
      </Col>
      <Col xs={24} xl={10}>
        <Card className="lingti-card" title="当前选择">
          <Space direction="vertical" size={14}>
            <Tag color="cyan">zh-CN</Tag>
            <Typography.Title level={3}>清晰女声</Typography.Title>
            <Typography.Paragraph>适合宣传片、产品介绍、服务讲解和品牌口播。</Typography.Paragraph>
            <Button type="primary" icon={<SoundOutlined />}>试听当前音色</Button>
          </Space>
        </Card>
      </Col>
    </Row>
  );
}

function UploadContent() {
  return (
    <Row gutter={[24, 24]}>
      <Col xs={24} lg={12}>
        <Card className="lingti-card" title="上传参考素材">
          <Upload.Dragger>
            <p className="ant-upload-drag-icon"><InboxOutlined /></p>
            <p className="ant-upload-text">上传人物图、产品图或参考视频</p>
            <p className="ant-upload-hint">支持 image/* 和 video/*，系统自动用于参考或截帧。</p>
          </Upload.Dragger>
        </Card>
      </Col>
      <Col xs={24} lg={12}>
        <Card className="lingti-card" title="素材清单">
          <Descriptions column={1}>
            <Descriptions.Item label="人物参考图">character-reference.png</Descriptions.Item>
            <Descriptions.Item label="产品参考图">product-shot.jpg</Descriptions.Item>
            <Descriptions.Item label="对标视频">reference-video.mp4</Descriptions.Item>
            <Descriptions.Item label="素材状态">已上传，等待工作流使用</Descriptions.Item>
          </Descriptions>
        </Card>
      </Col>
    </Row>
  );
}

function TaskCenterContent() {
  return (
    <Card className="lingti-card" title="任务中心">
      <Table
        pagination={false}
        dataSource={[
          { key: "1", title: "智慧康养宣传片", status: "视频生成中", action: "查看详情" },
          { key: "2", title: "酒店服务介绍", status: "等待脚本审核", action: "继续审核" },
          { key: "3", title: "产品功能短片", status: "已完成", action: "下载成片" },
          { key: "4", title: "企业形象片", status: "失败待恢复", action: "恢复任务" },
        ]}
        columns={[
          { title: "项目名称", dataIndex: "title" },
          { title: "任务状态", dataIndex: "status", render: (text) => <Tag color={text === "已完成" ? "green" : text === "失败待恢复" ? "red" : "blue"}>{text}</Tag> },
          { title: "操作", dataIndex: "action", render: (text) => <Button size="small">{text}</Button> },
        ]}
      />
    </Card>
  );
}

function ScriptContent() {
  return (
    <Card className="lingti-card" title="脚本审核与分镜">
      <Space direction="vertical" size={14} style={{ width: "100%" }}>
        {["开场介绍", "服务展示", "成片收束"].map((title, index) => (
          <Card key={title} size="small" className="lingti-mini-card">
            <Space direction="vertical" size={8}>
              <Space><Tag color="blue">Scene {index + 1}</Tag><Typography.Text strong>{title}</Typography.Text></Space>
              <Typography.Paragraph style={{ marginBottom: 0 }}>旁白：展示现代化服务场景，突出高端、智能和可信赖的品牌气质。</Typography.Paragraph>
              <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>画面提示词：高端商业宣传片风格，暖色自然光，人物真实，镜头平稳。</Typography.Paragraph>
            </Space>
          </Card>
        ))}
        <Space><Button type="primary" icon={<SaveOutlined />}>保存脚本</Button><Button icon={<PlayCircleOutlined />}>审核通过并继续</Button></Space>
      </Space>
    </Card>
  );
}

function ProgressContent() {
  return (
    <Card className="lingti-card" title="流程进度">
      <Space direction="vertical" size={18} style={{ width: "100%" }}>
        <Steps current={5} items={["脚本", "审核", "资产", "关键帧", "配音", "视频", "组装", "完成"].map((title) => ({ title }))} />
        <Progress percent={72} status="active" />
        <Alert type="info" showIcon message="正在生成第 3 段视频片段" description="视频生成链路会按分镜逐段处理，并将结果交给后续组装阶段。" />
      </Space>
    </Card>
  );
}

function LogsContent() {
  return (
    <Card className="lingti-card" title="生成日志">
      <Timeline
        items={[
          { color: "green", children: "脚本生成完成，等待审核" },
          { color: "green", children: "人物、场景、道具资产已生成" },
          { color: "green", children: "关键帧与配音文件已生成" },
          { color: "blue", children: "正在生成第 3 段视频片段" },
          { color: "gray", children: "后续将进入视频组装与字幕处理阶段" },
        ]}
      />
    </Card>
  );
}

function ResultContent() {
  return (
    <Card className="lingti-card" title="成片结果">
      <Row gutter={[24, 24]} align="middle">
        <Col xs={24} lg={10}><div className="demo-video-preview"><PlayCircleOutlined /><span>成片预览</span></div></Col>
        <Col xs={24} lg={14}>
          <Space direction="vertical" size={14}>
            <Typography.Paragraph>系统完成组装后，可在此预览视频、下载无字幕版、下载带字幕版，并导出剪映草稿。</Typography.Paragraph>
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
  );
}

function AnalysisResultContent() {
  return (
    <Row gutter={[24, 24]}>
      <Col xs={24} xl={10}>
        <Card className="lingti-card" title="整体分析">
          <Descriptions column={1}>
            <Descriptions.Item label="标题">智慧康养服务宣传片</Descriptions.Item>
            <Descriptions.Item label="比例">9:16</Descriptions.Item>
            <Descriptions.Item label="时长">60 秒</Descriptions.Item>
            <Descriptions.Item label="风格">温暖、高端、真实人物、柔和镜头</Descriptions.Item>
          </Descriptions>
        </Card>
      </Col>
      <Col xs={24} xl={14}>
        <Card className="lingti-card" title="分析出的分镜">
          <Timeline items={[
            { children: "开场环境镜头：现代化养老社区与温暖自然光" },
            { children: "人物活动镜头：休闲、交流、健康管理服务" },
            { children: "品牌收束镜头：服务口号与成片结束页" },
          ]} />
        </Card>
      </Col>
    </Row>
  );
}

function ConfigContent() {
  return (
    <Row gutter={[24, 24]}>
      <Col xs={24} xl={8}>
        <Card className="lingti-card" title="当前默认配置">
          <Descriptions column={1}>
            <Descriptions.Item label="LLM">OpenAI / gpt-4.1</Descriptions.Item>
            <Descriptions.Item label="图像">MiniMax / image-01</Descriptions.Item>
            <Descriptions.Item label="TTS">MiniMax / speech-02</Descriptions.Item>
            <Descriptions.Item label="视频">Kling / 1080p</Descriptions.Item>
          </Descriptions>
        </Card>
      </Col>
      <Col xs={24} xl={16}>
        <Card className="lingti-card" title="编辑配置">
          <Table
            pagination={false}
            dataSource={[
              { key: "1", item: "LLM API Key", status: "已配置", action: "测试" },
              { key: "2", item: "图片生成 Key", status: "已配置", action: "测试" },
              { key: "3", item: "TTS Key", status: "已配置", action: "测试" },
              { key: "4", item: "视频生成 Key", status: "已配置", action: "测试" },
            ]}
            columns={[
              { title: "配置项", dataIndex: "item" },
              { title: "状态", dataIndex: "status", render: (text) => <Tag color="green">{text}</Tag> },
              { title: "操作", dataIndex: "action", render: (text) => <Button size="small">{text}</Button> },
            ]}
          />
        </Card>
      </Col>
    </Row>
  );
}
