import { contextBridge, ipcRenderer } from 'electron';

// Expose protected methods that allow the renderer process to use
// ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Add any APIs you want to expose to the renderer process
  exportToPDF: (html: string) => ipcRenderer.invoke('export-to-pdf', html),
  saveFile: (data: any, filename: string) => ipcRenderer.invoke('save-file', data, filename)
});

export {};
