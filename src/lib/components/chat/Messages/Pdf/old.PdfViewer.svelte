<script lang="ts">
	//import { showPdfViewer } from '$lib/stores';
	import ChevronLeft from '$lib/components/icons/ChevronLeft.svelte';
	import ChevronRight from '$lib/components/icons/ChevronRight.svelte';
	import { getContext, onMount, setContext } from 'svelte';

	import { chatId } from '$lib/stores';
	//export let showPdfViewer; // Now we receive this as a prop
	export let selectedCitation;

	let showPdfViewer = getContext("showPdfViewer-"+$chatId);
	function togglePdf() {
		showPdfViewer.update(value => !value);
		console.log('Toggled PDF, new value:', $chatId, $showPdfViewer); // Debugging log
	}
</script>

<!-- PDF Viewer -->
<div
  class="h-full w-full border rounded-xl overflow-hidden bg-white transition-[opacity,width] duration-300 ease-in-out"
  style="width: {$showPdfViewer ? '100%' : '0'}; opacity: {$showPdfViewer ? '1' : '0'}; position: relative; top: 0; z-index: 9999;"
>
{#if $showPdfViewer}
	<iframe
		src={`/uploads/${selectedCitation?.pdfPath}#page=${selectedCitation?.page_number}#toolbar=0&navpanes=0`}
		type="application/pdf"
		class="w-full h-full"
	></iframe>
{/if}
</div>
