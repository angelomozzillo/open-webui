<script lang="ts">
	import { getContext, onMount, afterUpdate } from 'svelte';
	import { chatId } from '$lib/stores';

	export let selectedCitation;

	let showPdfViewer = getContext('showPdfViewer-' + $chatId);
	
	let highlightedPdfUrl = '';

	// Function to fetch the highlighted PDF
	async function fetchHighlightedPdf() {
		console.log('Highlighting...')
		if (!selectedCitation || !selectedCitation.pdfPath) return;

		let search_text = selectedCitation?.search_text;
		let page_num = selectedCitation?.page_number;

		const response = await fetch(`/uploads/${selectedCitation.pdfPath}`);
		const blob = await response.blob(); // Convert to Blob
		const pdfFile = new File([blob], selectedCitation.pdfPath, { type: "application/pdf" });

		console.log('FILE:', pdfFile)
		console.log(page_num, search_text)

		const formData = new FormData();
		formData.append('file', pdfFile); // Ensure selectedCitation has a File object
		formData.append("page_num", page_num.toString());
		formData.append("search_text", search_text || "");

		const highlightResponse = await fetch('/highlight/', {
			method: 'POST',
			body: formData
		});

		const highlightedBlob = await highlightResponse.blob();
		highlightedPdfUrl = URL.createObjectURL(highlightedBlob)+ `#page=${page_num}&zoom=90`;
		;
		console.log(highlightedPdfUrl)
	}

	// Fetch the PDF when selectedCitation changes
	$: selectedCitation, fetchHighlightedPdf();
</script>

<!-- PDF Viewer -->
<div
	class="h-full w-full border rounded-xl overflow-hidden bg-white transition-[opacity,width] duration-300 ease-in-out"
	style="width: {$showPdfViewer ? '100%' : '0'}; opacity: {$showPdfViewer
		? '1'
		: '0'}; position: relative; top: 0; z-index: 9999; border-color: gray;"
>
	{#if $showPdfViewer}
		<iframe
			src={highlightedPdfUrl
				? highlightedPdfUrl
				: `/uploads/${selectedCitation?.pdfPath}#page=${selectedCitation?.page_number}#zoom=80&toolbar=0&navpanes=0`}
			type="application/pdf"
			class="w-full h-full"
		></iframe>
	{/if}
</div>
