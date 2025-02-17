<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { chatId } from '$lib/stores';
	
	// Importing PDF.js
	import * as pdfjsLib from 'pdfjs-dist/webpack';
  
	export let selectedCitation;
  
	let showPdfViewer = getContext("showPdfViewer-"+$chatId);
	let viewerContainer;
  
	// Function to toggle PDF visibility
	function togglePdf() {
	  showPdfViewer.update(value => !value);
	  console.log('Toggled PDF, new value:', $chatId, $showPdfViewer);
	}
  
	// Set up pdf.js viewer
	const setupPdfViewer = async () => {
	  if (selectedCitation?.pdfPath) {
		const pdfUrl = `/uploads/${selectedCitation?.pdfPath}`;
  
		// Load PDF document
		const pdfDoc = await pdfjsLib.getDocument(pdfUrl).promise;
  
		// Initialize PDF.js viewer
		const viewer = viewerContainer.querySelector('.pdfViewer');
		const pdfViewer = new pdfjsLib.PDFViewer({
		  container: viewer,
		});
  
		// Set the document for the viewer
		pdfViewer.setDocument(pdfDoc);
	  }
	};
  
	onMount(() => {
	  setupPdfViewer();
	});
  </script>
  
  <!-- PDF Viewer -->
  <div
	class="h-full w-full border rounded-xl overflow-hidden bg-white transition-[opacity,width] duration-300 ease-in-out"
	style="width: {$showPdfViewer ? '100%' : '0'}; opacity: {$showPdfViewer ? '1' : '0'}; position: relative; top: 0; z-index: 9999;"
  >
	{#if $showPdfViewer}
	  <div class="pdf-container" bind:this={viewerContainer}>
		<!-- PDF.js Viewer Container -->
		<div class="pdfViewer"></div>
	  </div>
	{/if}
  </div>
  
  <style>
	/* Container styling */
	.pdf-container {
	  position: relative;
	  width: 100%;
	  height: 100%;
	}
  
	/* You may need to import the PDF.js CSS or include it manually */
	@import 'pdfjs-dist/web/pdf_viewer.css';
  </style>
  