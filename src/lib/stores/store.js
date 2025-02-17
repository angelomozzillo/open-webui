import { writable } from 'svelte/store';

export const createShowPdfViewerStore = (initialState = false) => {
  return writable(initialState);
};