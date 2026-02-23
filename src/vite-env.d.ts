/// <reference types="vite/client" />

interface Window {
  electronAPI: {
    exportToPDF: (html: string) => Promise<string>;
    saveFile: (data: any, filename: string) => Promise<string>;
  };
}
