import type { Metadata } from "next";
import { Space_Grotesk } from "next/font/google";

import "./globals.css";
import { AppProvider } from "@/context/AppContext";
import { Navbar } from "@/components/Navbar";

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title: "Mumbai Local Delay Tracker",
  description: "Live delay tracking dashboard for Mumbai local railways",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${spaceGrotesk.variable} font-sans antialiased`}><AppProvider><Navbar />{children}</AppProvider></body>
    </html>
  );
}
