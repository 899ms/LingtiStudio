from __future__ import annotations

import os
import re
import struct
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "soft-copyright-output"
SCREENSHOTS = OUT / "screenshots"

SOFTWARE_NAME = "灵缇多链路平台AI视频在线制作平台"
SHORT_NAME = "灵缇AI视频制作平台"
VERSION = "V1.0"
DEMO_URL = "http://localhost:3000"
APPLICANT = "苏州瑞立思科技有限公司"
CREDIT_CODE = "91320506MA1X6LD52Q"
SOURCE_LINES = "约14494行"


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        sig = f.read(24)
    if sig[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a png: {path}")
    return struct.unpack(">II", sig[16:24])


def text_run(text: str, *, bold: bool = False, size: int = 24, font: str = "宋体") -> str:
    props = [f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:eastAsia="{font}"/>', f'<w:sz w:val="{size}"/>', f'<w:szCs w:val="{size}"/>']
    if bold:
        props.append("<w:b/>")
    safe = escape(text)
    return f"<w:r><w:rPr>{''.join(props)}</w:rPr><w:t xml:space=\"preserve\">{safe}</w:t></w:r>"


def paragraph(text: str = "", *, style: str | None = None, bold: bool = False, size: int = 24, align: str | None = None, page_break: bool = False, font: str = "宋体") -> str:
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    ppr_xml = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    br = '<w:r><w:br w:type="page"/></w:r>' if page_break else ""
    return f"<w:p>{ppr_xml}{br}{text_run(text, bold=bold, size=size, font=font) if text else ''}</w:p>"


def image_paragraph(rel_id: str, title: str, image_path: Path, width_in: float = 6.2) -> str:
    w, h = png_size(image_path)
    width_emu = int(width_in * 914400)
    height_emu = int(width_emu * h / w)
    docpr_id = re.sub(r"\D", "", rel_id) or "1"
    name = escape(title)
    return f"""
<w:p>
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
        <wp:extent cx="{width_emu}" cy="{height_emu}"/>
        <wp:docPr id="{docpr_id}" name="{name}"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr><pic:cNvPr id="{docpr_id}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>
              <pic:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
              <pic:spPr>
                <a:xfrm><a:off x="0" y="0"/><a:ext cx="{width_emu}" cy="{height_emu}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
"""


def base_parts(document_xml: str, rels_xml: str, content_types: str) -> dict[str, bytes]:
    styles = """
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="宋体" w:hAnsi="宋体" w:eastAsia="宋体"/><w:sz w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr><w:rPr><w:rFonts w:ascii="宋体" w:hAnsi="宋体" w:eastAsia="宋体"/><w:b/><w:sz w:val="36"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:pPr><w:spacing w:before="260" w:after="160"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:rFonts w:ascii="宋体" w:hAnsi="宋体" w:eastAsia="宋体"/><w:b/><w:sz w:val="30"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:pPr><w:spacing w:before="160" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:rFonts w:ascii="宋体" w:hAnsi="宋体" w:eastAsia="宋体"/><w:b/><w:sz w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:eastAsia="宋体"/><w:sz w:val="16"/></w:rPr></w:style>
</w:styles>
"""
    return {
        "[Content_Types].xml": content_types.encode(),
        "_rels/.rels": b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""",
        "word/_rels/document.xml.rels": rels_xml.encode(),
        "word/document.xml": document_xml.encode(),
        "word/styles.xml": styles.encode(),
    }


def write_docx(path: Path, body_parts: list[str], images: list[Path] | None = None) -> None:
    images = images or []
    rel_entries = ['<Relationship Id="rStyle" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    overrides = [
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Default Extension="png" ContentType="image/png"/>',
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>',
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>',
    ]
    for idx, image in enumerate(images, start=1):
        rel_entries.append(f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{image.name}"/>')
    rels_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{''.join(rel_entries)}</Relationships>"""
    content_types = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">{''.join(overrides)}</Types>"""
    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>{''.join(body_parts)}
    <w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>
  </w:body>
</w:document>"""
    parts = base_parts(document_xml, rels_xml, content_types)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data)
        for image in images:
            z.write(image, f"word/media/{image.name}")


def manual_doc() -> None:
    shots = [
        ("登录页", SCREENSHOTS / "01-login.png"),
        ("平台首页与退出入口", SCREENSHOTS / "02-home.png"),
        ("快速生成页面", SCREENSHOTS / "03-create.png"),
        ("专业工作台页面", SCREENSHOTS / "04-studio.png"),
        ("对标视频分析页面", SCREENSHOTS / "05-analyze.png"),
        ("系统设置与连接器页面", SCREENSHOTS / "06-settings.png"),
        ("任务详情、生成进度与成片结果页面", SCREENSHOTS / "07-demo-task.png"),
    ]
    body = [
        paragraph(SOFTWARE_NAME, style="Title"),
        paragraph("软件使用说明书", style="Title"),
        paragraph(VERSION, align="center"),
        paragraph("一、系统简介", style="Heading1"),
        paragraph(f"{SOFTWARE_NAME}面向 AI 视频在线制作、素材生产、分镜审核和成片交付场景，提供主题创意录入、脚本生成、脚本审核、参考素材上传、对标视频分析、关键帧生成、配音合成、视频片段生成、字幕组装、任务恢复、项目管理和系统连接器配置等能力。平台通过统一 Web 控制台管理多条生成链路，使运营人员和内容制作人员能够围绕同一视频项目完成创建、审核、恢复、下载和交付。"),
        paragraph("本说明书基于系统实际页面截图编写，页面展示的任务数据用于说明平台主要功能流程。"),
        paragraph("系统名称", bold=True),
        paragraph(SOFTWARE_NAME),
        paragraph("版本号", bold=True),
        paragraph(VERSION),
        paragraph("访问方式", bold=True),
        paragraph("浏览器访问本地或部署后的 Web 控制台"),
        paragraph("演示地址", bold=True),
        paragraph(DEMO_URL),
        paragraph("演示账号", bold=True),
        paragraph("admin"),
        paragraph("二、运行环境与登录说明", style="Heading1"),
        paragraph("平台采用 Web 管理界面，用户通过浏览器访问系统地址并输入账号密码完成登录。登录成功后进入系统首页，主要模块通过左侧导航栏进入。系统登录入口用于保护视频项目、素材、配置和任务日志等业务数据。"),
        paragraph("退出登录入口位于左侧导航栏底部。用户点击“退出登录”后返回登录页面，系统清除本地登录状态，避免未授权人员继续访问视频制作工作台。"),
        paragraph("三、系统功能总览", style="Heading1"),
        paragraph("系统主要包括以下功能模块："),
        paragraph("登录与退出", bold=True),
        paragraph("提供账号密码登录、记住登录状态、返回首页和退出登录能力。"),
        paragraph("首页概览", bold=True),
        paragraph("集中展示系统状态、默认视频引擎、默认大语言模型、图片服务、TTS 模式和快速入口。"),
        paragraph("快速生成", bold=True),
        paragraph("面向普通运营人员，支持录入主题需求、风格描述、目标时长、画面比例、字幕开关、参考图和参考视频，并按推荐参数启动工作流。"),
        paragraph("专业工作台", bold=True),
        paragraph("面向内部制作与运维人员，集中提供新建任务、任务中心、脚本审核、进度查看、日志排错、恢复失败任务和下载成片等能力。"),
        paragraph("对标视频分析", bold=True),
        paragraph("支持上传参考视频，自动拆解人物、分镜、风格、提示词和整体节奏，并基于分析结果创建新的视频项目。"),
        paragraph("任务详情与生成进度", bold=True),
        paragraph("展示脚本、审核、资产、关键帧、配音、视频、组装和完成等阶段进度，支持查看任务信息、生成日志、脚本分镜和成片结果。"),
        paragraph("系统设置与连接器", bold=True),
        paragraph("维护 LLM、图片、TTS、视频生成平台等服务的默认 provider、模型、密钥和连接状态，支持保存配置和测试连接。"),
        paragraph("四、功能页面说明与截图", style="Heading1"),
    ]
    for idx, (title, image) in enumerate(shots, start=1):
        body.append(paragraph(f"{idx}. {title}", style="Heading2"))
        descriptions = {
            "登录页": "登录页提供账号、密码、记住登录状态和登录提交功能，用户完成登录后进入视频制作平台首页。",
            "平台首页与退出入口": "首页展示系统概览、主要功能入口和左侧导航栏，导航栏底部提供退出登录入口。",
            "快速生成页面": "快速生成页用于填写主题需求、风格、时长、画面比例、字幕和参考素材，适合快速发起 AI 视频任务。",
            "专业工作台页面": "专业工作台集中管理新建任务、任务中心、进行中任务、失败恢复和已完成任务。",
            "对标视频分析页面": "对标视频分析页用于上传参考视频，并在分析完成后生成分镜、人物、提示词和新项目创建参数。",
            "系统设置与连接器页面": "系统设置页展示系统健康、连接器状态、默认 provider、模型、音色目录和配置编辑表单。",
            "任务详情、生成进度与成片结果页面": "任务详情页展示脚本审核、生成进度、生成日志、任务信息和成片预览下载入口。",
        }
        body.append(paragraph(descriptions[title]))
        body.append(image_paragraph(f"rId{idx}", title, image))
    body.extend([
        paragraph("五、典型操作流程", style="Heading1"),
        paragraph("1. 用户访问系统地址，输入管理员账号和密码完成登录。"),
        paragraph("2. 在首页查看系统概览和默认服务配置，确认视频引擎、LLM、图片和 TTS 服务状态。"),
        paragraph("3. 在快速生成页输入主题需求、风格描述、目标时长、画面比例和字幕开关，并上传参考图或参考视频。"),
        paragraph("4. 需要精细控制时进入专业工作台，创建任务并查看任务中心中的进行中、失败和已完成项目。"),
        paragraph("5. 在任务详情页审核脚本分镜，确认人物、场景、道具、关键帧和配音等资产后继续生成。"),
        paragraph("6. 生成过程中查看实时进度和生成日志；如外部服务失败，可根据页面提供的动作恢复任务或重新组装。"),
        paragraph("7. 任务完成后预览成片，下载无字幕版、带字幕版或剪映草稿。"),
        paragraph("8. 在系统设置页维护 provider、模型、密钥、默认音色和运行配置。"),
        paragraph("9. 使用结束后点击左侧导航栏底部“退出登录”，返回登录页。"),
    ])
    write_docx(OUT / "说明书.docx", body, [p for _, p in shots])


def application_doc() -> None:
    body = [
        paragraph("计算机软件著作权登记申请表", style="Title"),
        paragraph("软件基本信息", style="Heading1"),
    ]
    fields = [
        ("软件名称", SOFTWARE_NAME),
        ("简称", SHORT_NAME),
        ("版本号", VERSION),
        ("开发完成时间", "2026年06月22日"),
        ("发表时间", "2026年06月22日"),
        ("发表省份/城市", "江苏省 苏州市 中国"),
        ("申请人名称", APPLICANT),
        ("统一信用代码", CREDIT_CODE),
        ("开发的硬件环境（限制字数50）", "CPU i5及以上，内存8GB及以上，硬盘256GB及以上"),
        ("运行的硬件环境（限制字数50）", "云服务器、物理服务器或本地开发主机，内存8GB及以上"),
        ("开发该软件的操作系统（限制字数50）", "Linux、macOS、Windows"),
        ("软件开发环境/开发工具（限制字数50）", "Python、FastAPI、Next.js、TypeScript、Node.js"),
        ("该软件的运行平台/操作系统（限制字数50）", "Linux、macOS、Windows及现代浏览器"),
        ("软件运行支撑环境/支持软件（限制字数50）", "Python、Node.js、FFmpeg、浏览器及外部AI服务接口"),
        ("编程语言", "Python、TypeScript、TSX、JavaScript"),
        ("源程序量", SOURCE_LINES),
        ("面向领域/行业（限制字数50）", "AI视频制作、内容生产、数字营销、在线创意工具"),
        ("软件分类", "☑应用软件 □嵌入式软件 □中间件 □操作系统"),
        ("开发目的（限制字数50）", "用于AI视频在线制作、分镜审核、素材生成和成片交付。"),
    ]
    for label, value in fields:
        body.append(paragraph(label, bold=True))
        body.append(paragraph(value))
    body.extend([
        paragraph("软件的主要功能（限制字数1300）", bold=True),
        paragraph(f"{SOFTWARE_NAME}是面向 AI 视频在线制作和多链路生成流程的 Web 应用软件。系统通过统一控制台组织视频项目创建、脚本生成、脚本审核、素材上传、对标视频分析、关键帧生成、配音合成、视频片段生成、字幕组装、任务恢复、成片下载和系统配置等工作。用户登录后可在首页查看系统状态、默认视频引擎、默认大语言模型、图片服务和 TTS 模式，并通过快速生成入口录入主题需求、风格描述、目标时长、画面比例、字幕开关和参考素材。专业工作台提供完整任务创建表单、任务中心、项目筛选、失败任务恢复和已完成任务下载能力。任务详情页按照脚本、审核、资产、关键帧、配音、视频、组装、完成等阶段展示进度，支持脚本标题修改、分镜审核、动作恢复、日志查看、视频预览、无字幕版下载、带字幕版下载和剪映草稿导出。对标视频分析模块可上传参考视频，分析人物、场景、风格、提示词和节奏，并基于分析结果创建新项目。系统设置模块用于维护 LLM、图片生成、TTS、Kling、MiniMax Video、Seedance 等服务连接器、默认模型、密钥状态、音色目录和配置文件。平台通过前端工作台、后端工作流编排、WebSocket 状态推送、外部 AI 服务路由和 FFmpeg 组装能力，实现从创意输入到成片交付的在线 AI 视频生产闭环。"),
        paragraph("软件的技术特点（请选择最多不超过3个）", bold=True),
        paragraph("☑云计算软件 □信息安全软件 ☑人工智能软件 □大数据软件 □5G软件 □小程序 □物联网软件 □智慧城市软件"),
        paragraph("软件的技术特点（限制字数100）", bold=True),
        paragraph("采用 FastAPI 工作流编排、Next.js Web 控制台、WebSocket 状态推送、多AI服务路由、FFmpeg 视频组装和配置化连接器管理技术。"),
    ])
    write_docx(OUT / "申请表模板.docx", body)


def source_doc() -> None:
    source_files = [
        "api/server.py",
        "core/config.py",
        "modules/llm.py",
        "modules/image_gen.py",
        "modules/tts.py",
        "modules/video_gen.py",
        "modules/assembler.py",
        "modules/jianying_draft.py",
        "frontend/lib/api.ts",
        "frontend/lib/types.ts",
        "frontend/app/page.tsx",
        "frontend/app/login/page.tsx",
        "frontend/app/demo/page.tsx",
        "frontend/components/workspace-layout.tsx",
        "frontend/components/create-project-form.tsx",
        "frontend/components/project-detail-client.tsx",
        "frontend/components/analysis-client.tsx",
        "frontend/components/settings-client.tsx",
        "frontend/components/projects-panel.tsx",
    ]
    body = []
    line_budget = 3200
    used = 0
    for rel in source_files:
        path = ROOT / rel
        if not path.exists() or used >= line_budget:
            continue
        header = f"// 文件：{rel}" if path.suffix in {".ts", ".tsx"} else f"# 文件：{rel}"
        body.append(paragraph(header, style="Code", font="Courier New", size=16))
        used += 1
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if used >= line_budget:
                break
            body.append(paragraph(line[:180], style="Code", font="Courier New", size=16))
            used += 1
        body.append(paragraph("", page_break=True))
    write_docx(OUT / "源代码.docx", body)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    manual_doc()
    application_doc()
    source_doc()
    print("generated:", OUT / "说明书.docx", OUT / "申请表模板.docx", OUT / "源代码.docx")
