<script lang="ts">
	//import { showPdfViewer } from '$lib/stores';
	import { getContext } from 'svelte';

	import { chatId } from '$lib/stores';
	//export let showPdfViewer; // Now we receive this as a prop
	export let selectedCitation;

	let showPdfViewer = getContext("showPdfViewer-"+$chatId);
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
