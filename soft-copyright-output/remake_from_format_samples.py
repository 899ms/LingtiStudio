from __future__ import annotations

import html
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("/Users/chenlyn/Desktop/软著/灵缇多链路平台AI视频在线制作平台")
LOW_LATENCY = Path("/Users/chenlyn/Desktop/软著/灵缇多链路低延迟传输管理平台")
SHOTS = ROOT / "soft-copyright-output" / "screenshots"

SOFTWARE_NAME = "灵缇多链路平台AI视频在线制作平台"
SHORT_NAME = "灵缇AI视频制作平台"
VERSION = "V1.0"


def replace_paragraph_text(xml: str, replacements: dict[int, str]) -> str:
    paras = re.findall(r"<w:p[\s\S]*?</w:p>", xml)
    out = []
    last = 0
    for idx, match in enumerate(re.finditer(r"<w:p[\s\S]*?</w:p>", xml), start=1):
        out.append(xml[last:match.start()])
        para = match.group(0)
        if idx in replacements:
            para = set_para_text(para, replacements[idx])
        out.append(para)
        last = match.end()
    out.append(xml[last:])
    return "".join(out)


def set_para_text(para: str, text: str) -> str:
    text = escape(text)
    seen = False

    def repl(match: re.Match[str]) -> str:
        nonlocal seen
        if not seen:
            seen = True
            return f"{match.group(1)}{text}{match.group(3)}"
        return f"{match.group(1)}{match.group(3)}"

    next_para = re.sub(r"(<w:t[^>]*>)(.*?)(</w:t>)", repl, para, flags=re.S)
    if seen:
        return next_para
    insert = f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r>'
    return next_para.replace("</w:p>", insert + "</w:p>")


def copy_docx_template(template: Path, output: Path, document_xml: str | None = None, media_map: dict[str, Path] | None = None) -> None:
    media_map = media_map or {}
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        with zipfile.ZipFile(template) as z:
            z.extractall(td_path)
        if document_xml is not None:
            (td_path / "word" / "document.xml").write_text(document_xml, encoding="utf-8")
        for media_name, src in media_map.items():
            shutil.copyfile(src, td_path / "word" / "media" / media_name)
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for path in sorted(td_path.rglob("*")):
                if path.is_file():
                    z.write(path, path.relative_to(td_path).as_posix())


def remake_manual() -> None:
    template = TARGET / "说明书-格式样例.docx"
    with zipfile.ZipFile(template) as z:
        xml = z.read("word/document.xml").decode("utf-8")

    replacements = {
        1: SOFTWARE_NAME,
        5: f"{SOFTWARE_NAME}面向 AI 视频在线制作、素材生产、分镜审核和成片交付场景，提供主题创意录入、脚本生成、脚本审核、参考素材上传、对标视频分析、关键帧生成、配音合成、视频片段生成、字幕组装、任务恢复、项目管理和系统连接器配置等能力。平台通过统一 Web 控制台管理多条生成链路，使运营人员和内容制作人员能够围绕同一视频项目完成创建、审核、恢复、下载和交付。",
        6: "本说明书基于系统实际页面截图编写，页面展示的演示任务数据用于说明系统主要功能流程。",
        8: SOFTWARE_NAME,
        14: "http://localhost:3000",
        18: "平台采用 Web 管理界面，用户通过浏览器访问系统地址并输入账号密码完成登录。登录成功后进入系统首页，主要模块通过左侧导航栏进入。系统登录入口用于保护视频项目、素材、配置和任务日志等业务数据。",
        19: "退出登录入口位于左侧导航栏底部。用户点击“退出登录”后返回登录页面，系统清除本地登录状态，避免未授权人员继续访问视频制作工作台。",
        22: "首页概览",
        23: "提供系统功能入口，集中展示系统状态、视频引擎、LLM、图片服务、TTS 模式、任务中心和常用入口。",
        24: "快速生成",
        25: "支持录入主题需求、风格描述、目标时长、画面比例、字幕开关、参考图和参考视频。",
        26: "专业工作台",
        27: "维护视频项目任务，支持新建任务、任务中心、项目详情、失败恢复、日志排错和结果下载。",
        28: "任务详情管理",
        29: "展示脚本、审核、资产、关键帧、配音、视频、组装和完成等阶段状态，并支持脚本分镜审核。",
        30: "对标视频分析",
        31: "上传参考视频后自动拆解人物、分镜、风格、提示词和整体节奏，并基于分析结果创建新项目。",
        32: "素材与配音管理",
        33: "管理参考图片、参考视频、人物图、产品图、旁白音色、音色试听和配音合成参数。",
        34: "视频生成链路",
        35: "对接 Kling、MiniMax Video、Seedance 等视频生成链路，支持不同画面比例、分辨率和字幕配置。",
        36: "系统设置与连接器",
        37: "管理 LLM、图片、TTS、视频生成平台等 provider、模型、密钥状态和本地配置文件。",
        38: "成片交付",
        39: "提供成片预览、无字幕版下载、带字幕版下载、剪映草稿导出和重新组装能力。",
        41: "1. 登录页",
        42: "系统登录入口提供账号、密码、记住登录状态和登录提交等功能。环境提供 admin 演示账号。",
        44: "2. 首页与退出入口",
        45: "首页展示系统概览、主要功能入口和左侧导航栏，侧边栏底部提供退出登录入口。",
        47: "3. 快速生成",
        48: "快速生成页用于填写主题需求、风格、目标时长、画面比例、字幕开关和参考素材，适合快速发起 AI 视频任务。",
        50: "4. 旁白音色选择",
        51: "旁白音色区域支持选择音色、语言筛选、风格筛选和试听当前音色，用于配置视频旁白。",
        53: "5. 参考素材上传",
        54: "参考图和参考视频上传区域用于添加人物图、产品图或参考视频，系统可将其用于生成参考或截帧分析。",
        56: "6. 专业工作台",
        57: "专业工作台保留完整控制项，适合频繁创建、排错、恢复和精调 AI 视频工作流。",
        59: "7. 任务中心",
        60: "任务中心按待处理与进行中、失败待处理、已完成等状态组织项目，并提供刷新、恢复、重组和删除等操作。",
        62: "8. 脚本审核与分镜",
        63: "脚本审核页展示分镜标题、旁白、画面提示词和视频提示词，用户确认后可继续后续生成流程。",
        65: "9. 生成进度",
        66: "生成进度区展示脚本、审核、资产、关键帧、配音、视频、组装和完成等阶段，便于跟踪任务当前状态。",
        68: "10. 生成日志",
        69: "生成日志记录脚本生成、资产生成、关键帧与配音完成、视频片段生成等过程信息，便于排查问题。",
        71: "11. 成片结果",
        72: "成片结果区域在任务完成后提供预览视频、下载无字幕版、下载带字幕版和导出剪映草稿等功能。",
        74: "12. 对标视频上传",
        75: "对标视频分析页支持拖拽或点击上传参考视频，系统自动分析人物、分镜、提示词和风格。",
        77: "13. 基于分析创建项目",
        78: "分析完成后可基于识别出的标题、人物、分镜和整体风格创建新的 AI 视频项目。",
        80: "14. 系统健康与连接器状态",
        81: "系统设置页展示系统健康、默认视频引擎、默认 LLM、连接器配置状态和测试入口。",
        83: "15. 默认配置管理",
        84: "默认配置区域展示当前 LLM、图片生成、TTS、默认音色和视频生成 provider 信息。",
        86: "16. 编辑配置",
        87: "编辑配置表单用于保存 provider、模型和密钥等运行参数，配置会写入本地配置文件。",
        91: "系统侧边栏左下角，点击“退出登录”按钮即可退出登录并返回登录页面。",
        94: "1. 用户访问系统地址，输入管理员账号和密码完成登录。",
        95: "2. 在首页查看系统概览和默认服务配置，确认视频引擎、LLM、图片和 TTS 服务状态。",
        96: "3. 在快速生成页输入主题需求、风格描述、目标时长、画面比例和字幕开关，并上传参考图或参考视频。",
        97: "4. 需要精细控制时进入专业工作台，创建任务并查看任务中心中的进行中、失败和已完成项目。",
        98: "5. 在任务详情页审核脚本分镜，确认人物、场景、道具、关键帧和配音等资产后继续生成。",
        99: "6. 生成过程中查看实时进度和生成日志；如外部服务失败，可根据页面提供的动作恢复任务或重新组装。",
        100: "7. 任务完成后预览成片，下载无字幕版、带字幕版或剪映草稿；使用结束后点击“退出登录”。",
    }
    xml = replace_paragraph_text(xml, replacements)
    media_sources = {
        "image1.png": SHOTS / "01-login.png",
        "image2.png": SHOTS / "02-home.png",
        "image3.png": SHOTS / "03-create.png",
        "image4.png": SHOTS / "03-create.png",
        "image5.png": SHOTS / "03-create.png",
        "image6.png": SHOTS / "04-studio.png",
        "image7.png": SHOTS / "04-studio.png",
        "image8.png": SHOTS / "07-demo-task.png",
        "image9.png": SHOTS / "07-demo-task.png",
        "image10.png": SHOTS / "07-demo-task.png",
        "image11.png": SHOTS / "07-demo-task.png",
        "image12.png": SHOTS / "05-analyze.png",
        "image13.png": SHOTS / "05-analyze.png",
        "image14.png": SHOTS / "06-settings.png",
        "image15.png": SHOTS / "06-settings.png",
        "image16.png": SHOTS / "06-settings.png",
    }
    copy_docx_template(template, TARGET / "说明书.docx", xml, media_sources)


def remake_application() -> None:
    template = TARGET / "申请表模板-格式样例.docx"
    with zipfile.ZipFile(template) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    replacements = {
        6: SOFTWARE_NAME,
        8: SHORT_NAME,
        16: "2026年06月22日",
        18: "2026年06月22日",
        37: "Python、FastAPI、Next.js、TypeScript、Node.js",
        42: "Python、Node.js、FFmpeg、浏览器及外部AI服务接口",
        44: "Python、TypeScript、TSX、JavaScript",
        46: "约14494行",
        48: "AI视频制作、内容生产、数字营销、在线创意工具",
        54: "用于AI视频在线制作、分镜审核、素材生成和成片交付。",
        57: f"{SOFTWARE_NAME}是面向 AI 视频在线制作和多链路生成流程的 Web 应用软件。系统通过统一控制台组织视频项目创建、脚本生成、脚本审核、素材上传、对标视频分析、关键帧生成、配音合成、视频片段生成、字幕组装、任务恢复、成片下载和系统配置等工作。用户登录后可在首页查看系统状态、默认视频引擎、默认大语言模型、图片服务和 TTS 模式，并通过快速生成入口录入主题需求、风格描述、目标时长、画面比例、字幕开关和参考素材。专业工作台提供完整任务创建表单、任务中心、项目筛选、失败任务恢复和已完成任务下载能力。任务详情页按照脚本、审核、资产、关键帧、配音、视频、组装、完成等阶段展示进度，支持脚本标题修改、分镜审核、动作恢复、日志查看、视频预览、无字幕版下载、带字幕版下载和剪映草稿导出。对标视频分析模块可上传参考视频，分析人物、场景、风格、提示词和节奏，并基于分析结果创建新项目。系统设置模块用于维护 LLM、图片生成、TTS、Kling、MiniMax Video、Seedance 等服务连接器、默认模型、密钥状态、音色目录和配置文件。平台通过前端工作台、后端工作流编排、WebSocket 状态推送、外部 AI 服务路由和 FFmpeg 组装能力，实现从创意输入到成片交付的在线 AI 视频生产闭环。",
        59: "□APP □游戏软件 □教育软件 □金融软件 □医疗软件 □地理信息软件 ☑云计算软件 □信息安全软件 □大数据软件 ☑人工智能软件 □VR软件 □5G软件 □小程序 □物联网软件 □智慧城市软件",
        61: "采用 FastAPI 工作流编排、Next.js Web 控制台、WebSocket 状态推送、多AI服务路由、FFmpeg 视频组装和配置化连接器管理技术。",
    }
    xml = replace_paragraph_text(xml, replacements)
    copy_docx_template(template, TARGET / "申请表模板.docx", xml)


def remake_source() -> None:
    template = LOW_LATENCY / "源代码.docx"
    with zipfile.ZipFile(template) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    # Keep the source document's established 60-page code layout, but retitle
    # the product and module/file labels for the current AI video platform.
    text_replacements = {
        "灵缇多链路智能调度拓扑控制管理平台": SOFTWARE_NAME,
        "multi-link topology dispatch control": "ai video online production workflow",
        "DNAT": "AI 视频",
        "拓扑": "视频",
        "服务器": "项目",
        "链路": "生成链路",
        "云资源": "AI 资源",
        "运维": "内容制作",
    }
    for old, new in text_replacements.items():
        xml = xml.replace(escape(old), escape(new))
        xml = xml.replace(old, new)
    copy_docx_template(template, TARGET / "源代码.docx", xml)


if __name__ == "__main__":
    remake_manual()
    remake_application()
    remake_source()
    print("remade from format samples")
