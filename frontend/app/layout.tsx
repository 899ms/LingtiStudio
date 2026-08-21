import type { Metadata } from "next";

import { Providers } from "@/components/providers";
import { SetupOnboarding } from "@/components/setup-onboarding";
import { WorkspaceLayout } from "@/components/workspace-layout";

import "./globals.css";

export const metadata: Metadata = {
  title: "灵缇多链路平台AI视频在线制作平台",
  description: "AI 在线视频制作与多链路生成工作流平台"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="zh-CN">
      <body suppressHydrationWarning>
        <Providers>
          <WorkspaceLayout>
            <SetupOnboarding />
            {children}
          </WorkspaceLayout>
        </Providers>
      </body>
    </html>
  );
}
